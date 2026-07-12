from __future__ import annotations

import argparse
import math
from pathlib import Path

import chess
import pandas as pd

from common import fen4, load_manifest


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


def load_direct_engine(model: str, device: str, multipv: int):
    """Use Maia-3's Python internals because the UCI text omits policy probabilities.

    This adapter intentionally fails loudly when the pinned API is unavailable rather
    than fabricating probabilities from MultiPV ranks.
    """
    try:
        from maia3.uci import Maia3UCIEngine, parse_args
    except ImportError as exc:
        raise RuntimeError(
            "Maia-3 is not installed. Install the pinned repository revision documented in LAB/README_LAB.md."
        ) from exc
    argv = [
        "--model", model,
        "--device", device,
        "--multipv", str(multipv),
        "--temperature", "0",
        "--top-p", "1",
        "--use-uci-history",
    ]
    if device == "cpu":
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


def profile(manifest_path: Path, model: str, device: str, elos: list[int], multipv: int) -> pd.DataFrame:
    manifest = load_manifest(manifest_path)
    engine = load_direct_engine(model, device, multipv)
    rows: list[dict] = []
    for record in manifest.to_dict("records"):
        set_position_from_record(engine, record)
        fen = record["fen_after_key_move"]
        for elo in elos:
            engine.self_elo = elo
            engine.oppo_elo = elo
            _chosen, top_moves = engine.score_moves()
            probs = [float(item["policy"]) for item in top_moves]
            entropy = normalized_entropy(probs)
            mass = sum(probs)
            for rank, item in enumerate(top_moves, start=1):
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
                    "topk_policy_mass": mass,
                    "normalized_response_entropy_topk": entropy,
                    "wdl_win_permille": win,
                    "wdl_draw_permille": draw,
                    "wdl_loss_permille": loss,
                    "fen": fen,
                    "status": "MODEL_PREDICTION_NOT_EMPIRICAL",
                })
    return pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Profile likely human responses using Maia-3 policy probabilities.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--model", default="maia3-79m")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--elos", nargs="+", type=int, default=[1100,1300,1500,1700,1900,2100])
    parser.add_argument("--multipv", type=int, default=10)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    df = profile(args.manifest, args.model, args.device, args.elos, args.multipv)
    df.to_csv(args.output, index=False)
    print(f"Wrote {len(df)} Maia-3 predictions to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
