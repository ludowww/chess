from __future__ import annotations

import csv
import io
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, TextIO

import chess
import chess.pgn
import pandas as pd


def fen4(value: str | chess.Board) -> str:
    """Return the four-field position key used by the Lichess evaluation export."""
    fen = value.fen() if isinstance(value, chess.Board) else value
    fields = fen.strip().split()
    if len(fields) < 4:
        raise ValueError(f"Invalid FEN: {fen!r}")
    return " ".join(fields[:4])


def load_manifest(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    df = pd.read_csv(path)
    required = {
        "line_id",
        "fen_before_key_move",
        "fen_after_key_move",
        "key_move_uci",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Manifest missing columns: {', '.join(missing)}")
    if df["line_id"].duplicated().any():
        dupes = df.loc[df["line_id"].duplicated(), "line_id"].tolist()
        raise ValueError(f"Duplicate line IDs: {dupes}")
    return df


def parse_pgn_games(path: str | Path) -> Iterator[chess.pgn.Game]:
    path = Path(path)
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        while True:
            game = chess.pgn.read_game(handle)
            if game is None:
                break
            yield game


@contextmanager
def open_text_maybe_zst(path: str | Path) -> Iterator[TextIO]:
    """Open a plain PGN or a .zst-compressed PGN as a streaming text file."""
    path = Path(path)
    if path.suffix.lower() != ".zst":
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            yield handle
        return

    try:
        import zstandard as zstd
    except ImportError as exc:
        raise RuntimeError(
            "Reading .zst requires the optional 'zstandard' package."
        ) from exc

    raw = path.open("rb")
    reader = zstd.ZstdDecompressor().stream_reader(raw)
    text = io.TextIOWrapper(reader, encoding="utf-8", errors="replace")
    try:
        yield text
    finally:
        text.close()
        raw.close()


def elo_band(elo: int, bands: list[tuple[int, int]]) -> tuple[int, int] | None:
    for low, high in bands:
        if low <= elo <= high:
            return low, high
    return None


def game_speed(headers: chess.pgn.Headers) -> str:
    """Prefer the Lichess Event label; fall back to an estimated time-control bucket."""
    event = headers.get("Event", "").lower()
    for speed in ("bullet", "blitz", "rapid", "classical"):
        if speed in event:
            return speed

    tc = headers.get("TimeControl", "")
    try:
        base_s, inc_s = tc.split("+", 1)
        effective = int(base_s) + 40 * int(inc_s)
    except (ValueError, AttributeError):
        return "unknown"
    if effective < 180:
        return "bullet"
    if effective < 480:
        return "blitz"
    if effective < 1500:
        return "rapid"
    return "classical"


def safe_int(value: str | None) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def score_cp(info: dict, pov: chess.Color) -> int:
    score = info.get("score")
    if score is None:
        raise ValueError("Engine result did not include a score")
    value = score.pov(pov).score(mate_score=100000)
    if value is None:
        raise ValueError("Could not convert engine score")
    return int(value)
