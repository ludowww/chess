from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

import chess.pgn
import pandas as pd

from common import parse_pgn_games


def max_rows(audit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for line_id, group in audit.groupby("line_id"):
        group = group.copy()
        group["loss_for_black_cp"] = group["loss_for_black_cp"].astype(int)
        row = group.sort_values(["loss_for_black_cp", "ply"], ascending=[False, True]).iloc[0]
        review = int((group["loss_for_black_cp"] > 25).sum())
        reject = int((group["loss_for_black_cp"] > 50).sum())
        rows.append({
            "line_id": line_id,
            "black_moves": int(len(group)),
            "black_moves_review": review,
            "black_moves_reject": reject,
            "max_loss_cp": int(row["loss_for_black_cp"]),
            "max_loss_ply": int(row["ply"]),
            "max_loss_move_uci": row["move_uci"],
            "max_loss_move_san": row["move_san"],
            "gate": "PASS" if int(row["loss_for_black_cp"]) <= 25 else "REVIEW" if int(row["loss_for_black_cp"]) <= 50 else "REJECT",
        })
    return pd.DataFrame(rows).sort_values("line_id")


def append_bilan_comments(pgn_path: Path, audit_path: Path, out_path: Path) -> None:
    audit = pd.read_csv(audit_path)
    maxima = max_rows(audit).set_index("line_id")
    games = list(parse_pgn_games(pgn_path))
    with out_path.open("w", encoding="utf-8") as handle:
        for game in games:
            line_id = game.headers.get("Round")
            if line_id not in maxima.index:
                raise ValueError(f"No audit maximum for {line_id}")
            m = maxima.loc[line_id]
            comment = f"BILAN V1.1 — Coup noir maximal : {int(m['max_loss_cp'])} cp. Gate : {m['gate']}."
            if int(m["max_loss_cp"]) > 15:
                comment += f" Ply {int(m['max_loss_ply'])}, coup {m['max_loss_move_san']}."
            game.comment = (game.comment + "\n" if game.comment else "") + comment
            exporter = chess.pgn.StringExporter(headers=True, variations=False, comments=True)
            handle.write(game.accept(exporter).strip() + "\n\n")


def write_summary(audit_path: Path, manifest_path: Path, out_path: Path) -> dict:
    audit = pd.read_csv(audit_path)
    manifest = pd.read_csv(manifest_path)
    maxima = max_rows(audit)
    source_map = manifest.set_index("line_id")["source_line_id"].to_dict()
    max_by_line = []
    for row in maxima.to_dict("records"):
        row["source_line_id"] = source_map.get(row["line_id"], "")
        max_by_line.append(row)
    summary = {
        "audit_file": str(audit_path),
        "nodes": int(audit["nodes"].max()) if "nodes" in audit else None,
        "multipv": 8,
        "engine_id": str(audit["engine_id"].dropna().iloc[0]) if "engine_id" in audit and not audit.empty else "Stockfish",
        "candidate_lines": int(len(manifest)),
        "black_moves_total": int(len(audit)),
        "black_moves_review": int((audit["loss_for_black_cp"].astype(int) > 25).sum()),
        "black_moves_reject": int((audit["loss_for_black_cp"].astype(int) > 50).sum()),
        "candidate_gate": "PASS" if int((audit["loss_for_black_cp"].astype(int) > 25).sum()) == 0 else "REVIEW_OR_REJECT",
        "max_by_line": max_by_line,
    }
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def verify_bilans(pgn_path: Path, audit_path: Path) -> None:
    maxima = max_rows(pd.read_csv(audit_path)).set_index("line_id")
    for game in parse_pgn_games(pgn_path):
        line_id = game.headers.get("Round")
        expected = f"Coup noir maximal : {int(maxima.loc[line_id, 'max_loss_cp'])} cp"
        if expected not in (game.comment or ""):
            raise AssertionError(f"BILAN mismatch for {line_id}: expected {expected!r}, got {game.comment!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pgn", type=Path, default=Path("PGN/99_cours_v1_1_candidate.pgn"))
    parser.add_argument("--audit", type=Path, default=Path("DATA/stockfish_v1_1_candidate_500k.csv"))
    parser.add_argument("--manifest", type=Path, default=Path("DATA/core_v1_1_candidate_manifest.csv"))
    parser.add_argument("--summary", type=Path, default=Path("DATA/v1_1_candidate_engine_summary.json"))
    args = parser.parse_args()
    append_bilan_comments(args.pgn, args.audit, args.pgn)
    summary = write_summary(args.audit, args.manifest, args.summary)
    verify_bilans(args.pgn, args.audit)
    print(f"finalized bilans; gate={summary['candidate_gate']} review={summary['black_moves_review']} reject={summary['black_moves_reject']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
