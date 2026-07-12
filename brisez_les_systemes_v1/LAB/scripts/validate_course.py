from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import chess
import chess.pgn

from common import load_manifest, parse_pgn_games


def validate(pgn_path: Path, manifest_path: Path) -> dict:
    manifest = load_manifest(manifest_path)
    expected = set(manifest["line_id"])
    found: list[str] = []
    errors: list[str] = []
    plies: list[int] = []

    for game_no, game in enumerate(parse_pgn_games(pgn_path), start=1):
        line_id = game.headers.get("Round", "")
        found.append(line_id)
        board = game.board()
        count = 0
        try:
            for move in game.mainline_moves():
                if move not in board.legal_moves:
                    raise ValueError(f"illegal move {move.uci()}")
                board.push(move)
                count += 1
        except Exception as exc:  # PGN-specific context is useful in the report.
            errors.append(f"game {game_no} / {line_id}: {exc}")
        plies.append(count)

    duplicates = sorted(k for k, v in Counter(found).items() if v > 1)
    missing = sorted(expected - set(found))
    unexpected = sorted(set(found) - expected)
    if duplicates:
        errors.append(f"duplicate IDs: {duplicates}")
    if missing:
        errors.append(f"missing manifest IDs: {missing}")
    if unexpected:
        errors.append(f"unexpected IDs: {unexpected}")

    return {
        "ok": not errors,
        "pgn": str(pgn_path),
        "manifest": str(manifest_path),
        "games": len(found),
        "unique_ids": len(set(found)),
        "min_plies": min(plies) if plies else 0,
        "max_plies": max(plies) if plies else 0,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pgn", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = validate(args.pgn, args.manifest)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
