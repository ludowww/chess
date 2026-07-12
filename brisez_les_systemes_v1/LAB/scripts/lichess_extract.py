from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path

import chess
import chess.pgn
import pandas as pd

from common import elo_band, fen4, game_speed, load_manifest, open_text_maybe_zst, safe_int


def extract(
    pgn_paths: list[Path],
    manifest_path: Path,
    bands: list[tuple[int, int]],
    speeds: set[str],
    split: str,
    max_games: int | None = None,
    max_plies: int | None = None,
) -> pd.DataFrame:
    manifest = load_manifest(manifest_path)
    positions: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for row in manifest.to_dict("records"):
        positions[fen4(row["fen_before_key_move"])].append((row["line_id"], "before_key", row["key_move_uci"]))
        positions[fen4(row["fen_after_key_move"])].append((row["line_id"], "after_key", ""))

    counts: Counter = Counter()
    totals: Counter = Counter()
    games_seen = 0

    for path in pgn_paths:
        with open_text_maybe_zst(path) as handle:
            while True:
                game = chess.pgn.read_game(handle)
                if game is None:
                    break
                games_seen += 1
                if max_games and games_seen > max_games:
                    break
                speed = game_speed(game.headers)
                if speed not in speeds:
                    continue
                white_elo = safe_int(game.headers.get("WhiteElo"))
                black_elo = safe_int(game.headers.get("BlackElo"))
                if white_elo is None or black_elo is None:
                    continue
                board = game.board()
                for ply_index, move in enumerate(game.mainline_moves(), start=1):
                    if max_plies and ply_index > max_plies:
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

    rows=[]
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
        df = df.sort_values(["line_id","position_role","elo_min","speed","frequency"], ascending=[True,True,True,True,False])
    print(f"Scanned {games_seen} games; matched {sum(totals.values())} target-position occurrences.")
    return df


def parse_band(value: str) -> tuple[int, int]:
    low, high = value.split("-", 1)
    return int(low), int(high)


def main() -> int:
    parser = argparse.ArgumentParser(description="Stream Lichess PGNs and count moves in target positions.")
    parser.add_argument("pgn", nargs="+", type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--bands", nargs="+", type=parse_band, default=[(1100,1299),(1300,1499),(1500,1699),(1700,1899),(1900,2099)])
    parser.add_argument("--speeds", nargs="+", default=["blitz","rapid"])
    parser.add_argument("--split", required=True, choices=["discovery","validation","test"])
    parser.add_argument("--max-games", type=int)
    parser.add_argument("--max-plies", type=int, help="Optional opening-only scan cutoff; target FENs are opening positions.")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    df = extract(args.pgn, args.manifest, args.bands, set(args.speeds), args.split, args.max_games, args.max_plies)
    df.to_csv(args.output, index=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
