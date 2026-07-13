from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import chess.pgn
import pandas as pd

from common import parse_pgn_games

STALE_BILAN_MARKERS = (
    "BILAN — Ligne",
    "Audit moteur des coups imposés",
    "perte maximale observée",
    "BILAN V1.1 —",
)


def clean_comment(comment: str) -> str:
    if not comment:
        return ""
    parts = [part.strip() for part in re.split(r"\n+", comment) if part.strip()]
    kept = [part for part in parts if not any(marker in part for marker in STALE_BILAN_MARKERS)]
    return "\n".join(kept).strip()


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


def bilan_text(row: pd.Series) -> str:
    text = f"BILAN V1.1 — Coup noir maximal : {int(row['max_loss_cp'])} cp. Gate : {row['gate']}."
    if int(row["max_loss_cp"]) > 15:
        text += f" Maximum au ply {int(row['max_loss_ply'])} sur ...{row['max_loss_move_san']}."
    return text


def regenerate_bilan_comments(pgn_path: Path, audit_path: Path, out_path: Path) -> None:
    audit = pd.read_csv(audit_path)
    maxima = max_rows(audit).set_index("line_id")
    games = list(parse_pgn_games(pgn_path))
    with out_path.open("w", encoding="utf-8") as handle:
        for game in games:
            line_id = game.headers.get("Round")
            if line_id not in maxima.index:
                raise ValueError(f"No audit maximum for {line_id}")
            game.comment = clean_comment(game.comment)
            last_node = game
            for node in game.mainline():
                node.comment = clean_comment(node.comment)
                last_node = node
            if last_node is game:
                raise ValueError(f"Game has no moves: {line_id}")
            b = bilan_text(maxima.loc[line_id])
            last_node.comment = (last_node.comment + "\n" if last_node.comment else "") + b
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
    stale = STALE_BILAN_MARKERS[:-1]
    for game in parse_pgn_games(pgn_path):
        line_id = game.headers.get("Round")
        comments = []
        last = game
        for node in game.mainline():
            if node.comment:
                comments.append((node, node.comment))
            last = node
        bilans = [(node, comment) for node, comment in comments if "BILAN V1.1 —" in comment]
        if len(bilans) != 1:
            raise AssertionError(f"Expected exactly one V1.1 bilan for {line_id}, got {len(bilans)}")
        if bilans[0][0] is not last:
            raise AssertionError(f"BILAN V1.1 is not on last node for {line_id}")
        all_comment_text = "\n".join(c for _, c in comments)
        for marker in stale:
            if marker in all_comment_text:
                raise AssertionError(f"Stale bilan marker {marker!r} in {line_id}")
        m = maxima.loc[line_id]
        expected = bilan_text(m)
        if bilans[0][1].count(expected) != 1:
            raise AssertionError(f"BILAN mismatch for {line_id}: expected {expected!r}, got {bilans[0][1]!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pgn", type=Path, default=Path("PGN/99_cours_v1_1_candidate.pgn"))
    parser.add_argument("--audit", type=Path, default=Path("DATA/stockfish_v1_1_candidate_500k.csv"))
    parser.add_argument("--manifest", type=Path, default=Path("DATA/core_v1_1_candidate_manifest.csv"))
    parser.add_argument("--summary", type=Path, default=Path("DATA/v1_1_candidate_engine_summary.json"))
    args = parser.parse_args()
    regenerate_bilan_comments(args.pgn, args.audit, args.pgn)
    summary = write_summary(args.audit, args.manifest, args.summary)
    verify_bilans(args.pgn, args.audit)
    print(f"finalized bilans; gate={summary['candidate_gate']} review={summary['black_moves_review']} reject={summary['black_moves_reject']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
