from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import chess
import chess.engine
import pandas as pd

from common import load_manifest, score_cp


def normalize_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Accept either Lichess frequencies or Maia-3 policy probabilities."""
    df = df.copy()
    if "position_role" not in df.columns:
        df["position_role"] = "after_key"
    if "frequency" not in df.columns:
        if "policy_probability" not in df.columns:
            raise ValueError("Distribution needs frequency or policy_probability")
        df["frequency"] = df["policy_probability"]
    if "source" not in df.columns:
        df["source"] = "maia3" if "policy_probability" in df.columns else "lichess"
    return df


def evaluate(distribution_path: Path, manifest_path: Path, engine_path: str, nodes: int) -> pd.DataFrame:
    if shutil.which(engine_path) is None and not Path(engine_path).exists():
        raise FileNotFoundError(f"Stockfish binary not found: {engine_path}")
    dist = normalize_distribution(pd.read_csv(distribution_path))
    manifest = load_manifest(manifest_path).set_index("line_id")
    dist = dist[dist["position_role"] == "after_key"].copy()
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    rows=[]
    try:
        for rec in dist.to_dict("records"):
            board = chess.Board(manifest.loc[rec["line_id"], "fen_after_key_move"] + " 0 1")
            move = chess.Move.from_uci(rec["move_uci"])
            if move not in board.legal_moves:
                continue
            pov = board.turn
            best = engine.analyse(board, chess.engine.Limit(nodes=nodes))
            cand = engine.analyse(board, chess.engine.Limit(nodes=nodes), root_moves=[move])
            best_cp = score_cp(best, pov)
            cand_cp = score_cp(cand, pov)
            loss = max(0, best_cp - cand_cp)
            rows.append({**rec,
                "move_san": board.san(move),
                "best_eval_mover_cp": best_cp,
                "candidate_eval_mover_cp": cand_cp,
                "response_loss_cp": loss,
                "response_quality": "OK" if loss < 40 else ("ERROR" if loss < 100 else "SEVERE_ERROR"),
                "nodes": nodes,
            })
    finally:
        engine.quit()
    return pd.DataFrame(rows)


def main() -> int:
    parser=argparse.ArgumentParser(description="Evaluate observed or Maia-predicted responses with Stockfish.")
    parser.add_argument("--distribution", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--engine", default="stockfish")
    parser.add_argument("--nodes", type=int, default=100000)
    parser.add_argument("--output", required=True, type=Path)
    args=parser.parse_args()
    df=evaluate(args.distribution,args.manifest,args.engine,args.nodes)
    df.to_csv(args.output,index=False)
    print(f"Wrote {len(df)} response evaluations to {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
