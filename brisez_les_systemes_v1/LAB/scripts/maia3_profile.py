from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any

import chess
import pandas as pd

from common import fen4, load_manifest


AMP_MODES = ("auto", "on", "off")


def fen6(fen: str) -> str:
    fields = fen.strip().split()
    if len(fields) == 4:
        return fen.strip() + " 0 1"
    if len(fields) == 6:
        return fen.strip()
    raise ValueError(f"Expected 4- or 6-field FEN, got {len(fields)} fields: {fen!r}")


def fixed_prefix_to_uci_history(fixed_prefix: str, line_id: str) -> tuple[chess.Board, list[str]]:
    board = chess.Board()
    history: list[str] = []
    try:
        for token in fixed_prefix.split():
            if token.endswith(".") or token.endswith("..."):
                continue
            move = board.parse_san(token)
            history.append(move.uci())
            board.push(move)
    except ValueError as exc:
        raise ValueError(f"Could not parse fixed_prefix for {line_id}: {fixed_prefix!r}") from exc
    return board, history


def position_from_fixed_prefix(record: dict) -> tuple[chess.Board, list[str]]:
    line_id = str(record.get("line_id", "<unknown>"))
    fixed_prefix = str(record.get("fixed_prefix", "") or "")
    board, history = fixed_prefix_to_uci_history(fixed_prefix, line_id)
    target = str(record["fen_after_key_move"])
    if fen4(board) != fen4(target):
        raise ValueError(
            f"Maia position mismatch for {line_id}: fixed_prefix gives {fen4(board)!r}, "
            f"manifest has {fen4(target)!r}"
        )
    return board, history


def set_position_from_record(engine, record: dict) -> None:
    board, history = position_from_fixed_prefix(record)
    command = "position startpos moves " + " ".join(history)
    engine.cmd_position(command)
    line_id = str(record.get("line_id", "<unknown>"))
    if fen4(engine.board) != fen4(record["fen_after_key_move"]):
        raise ValueError(
            f"Maia engine board mismatch for {line_id}: engine has {fen4(engine.board)!r}, "
            f"manifest has {fen4(record['fen_after_key_move'])!r}"
        )
    if fen4(engine.board) != fen4(board):
        raise ValueError(
            f"Maia engine did not preserve reconstructed history for {line_id}: "
            f"engine has {fen4(engine.board)!r}, reconstructed {fen4(board)!r}"
        )


def normalized_entropy(probs: list[float]) -> float:
    probs = [p for p in probs if p > 0]
    if len(probs) <= 1:
        return 0.0
    h = -sum(p * math.log(p) for p in probs)
    return h / math.log(len(probs))


def torch_metadata(device: str) -> dict[str, Any]:
    meta: dict[str, Any] = {
        "torch_version": "",
        "torch_cuda_version": "",
        "gpu_name": "",
        "peak_vram_bytes": 0,
    }
    try:
        import torch
    except ImportError:
        return meta
    meta["torch_version"] = str(getattr(torch, "__version__", ""))
    meta["torch_cuda_version"] = str(getattr(torch.version, "cuda", "") or "")
    if device.startswith("cuda") and torch.cuda.is_available():
        cuda_index = 0
        if ":" in device:
            try:
                cuda_index = int(device.split(":", 1)[1])
            except ValueError:
                cuda_index = 0
        meta["gpu_name"] = torch.cuda.get_device_name(cuda_index)
        try:
            meta["peak_vram_bytes"] = int(torch.cuda.max_memory_allocated(cuda_index))
        except Exception:
            meta["peak_vram_bytes"] = 0
    return meta


def reset_peak_vram(device: str) -> None:
    if not device.startswith("cuda"):
        return
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
    except Exception:
        return


def load_direct_engine(model: str, device: str, multipv: int, amp_mode: str = "auto"):
    """Use Maia-3's Python internals because the UCI text omits policy probabilities.

    This adapter intentionally fails loudly when the pinned API is unavailable rather
    than fabricating probabilities from MultiPV ranks. AMP is controlled only through
    Maia-3's documented CLI flags; no installed package files are modified.
    """
    try:
        from maia3.uci import Maia3UCIEngine, parse_args
    except ImportError as exc:
        raise RuntimeError(
            "Maia-3 is not installed. Install the pinned repository revision documented in LAB/README_LAB.md."
        ) from exc
    if amp_mode not in AMP_MODES:
        raise ValueError(f"Unsupported amp_mode: {amp_mode!r}")
    argv = [
        "--model", model,
        "--device", device,
        "--multipv", str(multipv),
        "--temperature", "0",
        "--top-p", "1",
        "--use-uci-history",
    ]
    if amp_mode == "off" or (amp_mode == "auto" and device == "cpu"):
        argv.append("--no-use-amp")
    cfg = parse_args(argv)
    engine = Maia3UCIEngine(cfg)
    engine.ensure_model_loaded()
    return engine


def set_position(engine, fen: str, history_uci: str = "") -> None:
    """Fallback helper for isolated tests that start from an explicit FEN."""
    command = f"position fen {fen6(fen)}"
    history_uci = history_uci.strip()
    if history_uci:
        command += f" moves {history_uci}"
    engine.cmd_position(command)


def set_engine_multipv(engine: Any, multipv: int) -> None:
    """Best-effort update for Maia-3 internals and test fakes."""
    for attr in ("multipv", "MultiPV"):
        if hasattr(engine, attr):
            try:
                setattr(engine, attr, multipv)
            except Exception:
                pass
    cfg = getattr(engine, "cfg", None)
    if cfg is not None and hasattr(cfg, "multipv"):
        try:
            setattr(cfg, "multipv", multipv)
        except Exception:
            pass


def profile(
    manifest_path: Path,
    model: str,
    device: str,
    elos: list[int],
    multipv: int,
    amp_mode: str = "auto",
    all_legal_moves: bool = False,
) -> pd.DataFrame:
    manifest = load_manifest(manifest_path)
    max_multipv = multipv
    if all_legal_moves:
        max_multipv = max(chess.Board(fen6(str(row["fen_after_key_move"]))).legal_moves.count() for _, row in manifest.iterrows())
    reset_peak_vram(device)
    started = time.perf_counter()
    engine = load_direct_engine(model, device, max_multipv, amp_mode=amp_mode)
    rows: list[dict] = []
    for record in manifest.to_dict("records"):
        set_position_from_record(engine, record)
        fen = record["fen_after_key_move"]
        legal_moves = {move.uci() for move in engine.board.legal_moves}
        requested_multipv = len(legal_moves) if all_legal_moves else multipv
        set_engine_multipv(engine, requested_multipv)
        for elo in elos:
            engine.self_elo = elo
            engine.oppo_elo = elo
            _chosen, top_moves = engine.score_moves()
            legal_items = [item for item in top_moves if item["move"].uci() in legal_moves]
            if all_legal_moves and len(legal_items) != len(legal_moves):
                missing = sorted(legal_moves - {item["move"].uci() for item in legal_items})
                raise ValueError(
                    f"Full-policy export for {record['line_id']} Elo {elo} returned "
                    f"{len(legal_items)}/{len(legal_moves)} legal moves; missing {missing[:10]}"
                )
            selected = legal_items if all_legal_moves else legal_items[:multipv]
            probs = [float(item["policy"]) for item in selected]
            entropy = normalized_entropy(probs)
            legal_policy_mass = sum(float(item["policy"]) for item in legal_items)
            topk_mass = sum(probs)
            if all_legal_moves and abs(legal_policy_mass - 1.0) > 1e-5:
                raise ValueError(
                    f"Legal policy mass for {record['line_id']} Elo {elo} is {legal_policy_mass:.12f}, expected 1.0"
                )
            for rank, item in enumerate(selected, start=1):
                move = item["move"]
                win, draw, loss = item["wdl"]
                rows.append({
                    "line_id": record["line_id"],
                    "bias_code": record.get("bias_code", ""),
                    "elo": elo,
                    "model": model,
                    "rank": rank,
                    "move_uci": move.uci(),
                    "move_san": engine.board.san(move),
                    "policy_probability": float(item["policy"]),
                    "topk_policy_mass": topk_mass,
                    "normalized_response_entropy_topk": entropy,
                    "wdl_win_permille": win,
                    "wdl_draw_permille": draw,
                    "wdl_loss_permille": loss,
                    "fen": fen,
                    "status": "MODEL_PREDICTION_NOT_EMPIRICAL",
                    "device": device,
                    "amp_mode": amp_mode,
                    "torch_version": "",
                    "torch_cuda_version": "",
                    "gpu_name": "",
                    "elapsed_seconds": 0.0,
                    "peak_vram_bytes": 0,
                    "legal_policy_mass": legal_policy_mass,
                })
    elapsed = time.perf_counter() - started
    meta = torch_metadata(device)
    for row in rows:
        row["elapsed_seconds"] = elapsed
        row.update(meta)
    return pd.DataFrame(rows)


def write_metadata_sidecar(output: Path, df: pd.DataFrame) -> None:
    if df.empty:
        return
    cols = [
        "device", "amp_mode", "torch_version", "torch_cuda_version", "gpu_name",
        "elapsed_seconds", "peak_vram_bytes", "legal_policy_mass",
    ]
    metadata = {c: df[c].iloc[0].item() if hasattr(df[c].iloc[0], "item") else df[c].iloc[0] for c in cols if c in df.columns}
    sidecar = output.with_suffix(output.suffix + ".metadata.json")
    sidecar.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Profile likely human responses using Maia-3 policy probabilities.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--model", default="maia3-79m")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--elos", nargs="+", type=int, default=[1100, 1300, 1500, 1700, 1900, 2100])
    parser.add_argument("--multipv", type=int, default=10)
    parser.add_argument("--amp-mode", choices=AMP_MODES, default="auto")
    parser.add_argument("--all-legal-moves", action="store_true")
    parser.add_argument("--output", required=True, type=Path)
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    df = profile(
        args.manifest,
        args.model,
        args.device,
        args.elos,
        args.multipv,
        amp_mode=args.amp_mode,
        all_legal_moves=args.all_legal_moves,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    write_metadata_sidecar(args.output, df)
    print(f"Wrote {len(df)} Maia-3 predictions to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
