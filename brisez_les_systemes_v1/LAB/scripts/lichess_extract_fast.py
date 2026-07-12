from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

import chess
import pandas as pd

from common import elo_band, fen4, game_speed, load_manifest, open_text_maybe_zst, safe_int

HEADER_RE = re.compile(r'^\[(\w+)\s+"(.*)"\]$')
COMMENT_RE = re.compile(r'\{[^}]*\}')
VAR_RE = re.compile(r'\([^()]*\)')
RESULTS = {"1-0", "0-1", "1/2-1/2", "*"}


def san_tokens(movetext: str):
    text = COMMENT_RE.sub(" ", movetext)
    # Lichess dumps should not contain variations, but strip shallow ones defensively.
    while "(" in text and ")" in text:
        new = VAR_RE.sub(" ", text)
        if new == text:
            break
        text = new
    text = re.sub(r"\$\d+", " ", text)
    text = re.sub(r"\d+\.(\.\.)?", " ", text)
    for token in text.split():
        token = token.strip()
        if not token or token in RESULTS:
            continue
        yield token


def iter_games(handle):
    headers: dict[str, str] = {}
    movelines: list[str] = []
    in_moves = False
    for raw in handle:
        line = raw.strip()
        if not line:
            if in_moves and headers:
                yield headers, " ".join(movelines)
                headers = {}
                movelines = []
                in_moves = False
            continue
        m = HEADER_RE.match(line)
        if m and not in_moves:
            headers[m.group(1)] = m.group(2)
        else:
            in_moves = True
            movelines.append(line)
    if in_moves and headers:
        yield headers, " ".join(movelines)


def extract(pgn_paths: list[Path], manifest_path: Path, bands: list[tuple[int, int]], speeds: set[str], split: str, max_games: int | None = None, max_plies: int = 80) -> pd.DataFrame:
    manifest = load_manifest(manifest_path)
    positions: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for row in manifest.to_dict("records"):
        positions[fen4(row["fen_before_key_move"])].append((row["line_id"], "before_key", row["key_move_uci"]))
        positions[fen4(row["fen_after_key_move"])].append((row["line_id"], "after_key", ""))

    counts: Counter = Counter()
    totals: Counter = Counter()
    games_seen = 0
    parse_errors = 0

    for path in pgn_paths:
        with open_text_maybe_zst(path) as handle:
            for headers, movetext in iter_games(handle):
                games_seen += 1
                if max_games and games_seen > max_games:
                    break
                speed = game_speed(headers)
                if speed not in speeds:
                    continue
                white_elo = safe_int(headers.get("WhiteElo"))
                black_elo = safe_int(headers.get("BlackElo"))
                if white_elo is None or black_elo is None:
                    continue
                board = chess.Board()
                for ply_index, token in enumerate(san_tokens(movetext), start=1):
                    if max_plies and ply_index > max_plies:
                        break
                    try:
                        move = board.parse_san(token)
                    except Exception:
                        parse_errors += 1
                        break
                    key = fen4(board)
                    hits = positions.get(key)
                    if hits:
                        mover_elo = white_elo if board.turn == chess.WHITE else black_elo
                        band = elo_band(mover_elo, bands)
                        if band:
                            low, high = band
                            for line_id, role, candidate in hits:
                                base = (line_id, role, low, high, speed, split)
                                totals[base] += 1
                                counts[base + (move.uci(),)] += 1
                    board.push(move)
            if max_games and games_seen > max_games:
                break

    rows = []
    for key, count in counts.items():
        line_id, role, low, high, speed, split_name, move_uci = key
        total = totals[(line_id, role, low, high, speed, split_name)]
        rows.append({
            "line_id": line_id,
            "position_role": role,
            "elo_min": low,
            "elo_max": high,
            "speed": speed,
            "split": split_name,
            "move_uci": move_uci,
            "count": count,
            "total_positions": total,
            "frequency": count / total if total else 0.0,
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(["line_id", "position_role", "elo_min", "speed", "frequency"], ascending=[True, True, True, True, False])
    print(f"Scanned {games_seen} games; matched {sum(totals.values())} target-position occurrences; parse_errors={parse_errors}.")
    return df


def parse_band(value: str) -> tuple[int, int]:
    low, high = value.split("-", 1)
    return int(low), int(high)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fast shallow stream extraction for Lichess PGNs.")
    parser.add_argument("pgn", nargs="+", type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--bands", nargs="+", type=parse_band, default=[(1100,1299),(1300,1499),(1500,1699),(1700,1899),(1900,2099)])
    parser.add_argument("--speeds", nargs="+", default=["blitz", "rapid"])
    parser.add_argument("--split", required=True, choices=["discovery", "validation", "test"])
    parser.add_argument("--max-games", type=int)
    parser.add_argument("--max-plies", type=int, default=80)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    df = extract(args.pgn, args.manifest, args.bands, set(args.speeds), args.split, args.max_games, args.max_plies)
    df.to_csv(args.output, index=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
