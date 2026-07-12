from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import chess
import chess.engine
import pandas as pd

from common import load_manifest, parse_pgn_games, score_cp


def grade(loss_cp: int, a: int, b: int, c: int) -> str:
    if loss_cp <= a:
        return "A"
    if loss_cp <= b:
        return "B"
    if loss_cp <= c:
        return "C"
    return "REVIEW"


def audit(
    pgn_path: Path,
    manifest_path: Path,
    engine_path: str,
    nodes: int,
    multipv: int,
    threads: int,
    hash_mb: int,
) -> pd.DataFrame:
    if shutil.which(engine_path) is None and not Path(engine_path).exists():
        raise FileNotFoundError(
            f"Stockfish binary not found: {engine_path}. Pass --engine /path/to/stockfish."
        )
    manifest = load_manifest(manifest_path).set_index("line_id")
    wanted = set(manifest.index)
    rows: list[dict] = []

    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    try:
        engine.configure({"Threads": threads, "Hash": hash_mb})
        for game in parse_pgn_games(pgn_path):
            line_id = game.headers.get("Round", "")
            if line_id not in wanted:
                continue
            board = game.board()
            for ply, move in enumerate(game.mainline_moves(), start=1):
                if board.turn != chess.BLACK:
                    board.push(move)
                    continue
                before = board.copy()
                best_infos = engine.analyse(
                    before,
                    chess.engine.Limit(nodes=nodes),
                    multipv=multipv,
                )
                if isinstance(best_infos, dict):
                    best_infos = [best_infos]
                candidate_info = engine.analyse(
                    before,
                    chess.engine.Limit(nodes=nodes),
                    root_moves=[move],
                )
                best_cp = score_cp(best_infos[0], chess.WHITE)
                candidate_cp = score_cp(candidate_info, chess.WHITE)
                loss = max(0, candidate_cp - best_cp)
                rank = None
                for idx, info in enumerate(best_infos, start=1):
                    pv = info.get("pv") or []
                    if pv and pv[0] == move:
                        rank = idx
                        break
                rows.append({
                    "line_id": line_id,
                    "ply": ply,
                    "fen_before": before.fen(),
                    "move_uci": move.uci(),
                    "move_san": before.san(move),
                    "rank_multipv": rank,
                    "best_eval_white_cp": best_cp,
                    "candidate_eval_white_cp": candidate_cp,
                    "loss_for_black_cp": loss,
                    "grade": grade(loss, 25, 50, 80),
                    "nodes": nodes,
                    "engine_id": engine.id.get("name", "Stockfish"),
                })
                board.push(move)
    finally:
        engine.quit()
    return pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Reproducible Stockfish audit of all Black moves.")
    parser.add_argument("--pgn", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--engine", default="stockfish")
    parser.add_argument("--nodes", type=int, default=50000)
    parser.add_argument("--multipv", type=int, default=8)
    parser.add_argument("--threads", type=int, default=2)
    parser.add_argument("--hash-mb", type=int, default=512)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    df = audit(args.pgn, args.manifest, args.engine, args.nodes, args.multipv, args.threads, args.hash_mb)
    df.to_csv(args.output, index=False)
    print(f"Wrote {len(df)} audited moves to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
