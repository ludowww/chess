from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import chess
import pandas as pd

from common import fen4

GROUP_COLS = ["line_id", "elo"]


@dataclass
class ComparisonResult:
    details: pd.DataFrame
    summary: dict


def _ranked(group: pd.DataFrame) -> pd.DataFrame:
    return group.sort_values(["rank", "move_uci"], kind="stable").reset_index(drop=True)


def _spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 2:
        return None
    sx = pd.Series(xs).rank(method="average").to_list()
    sy = pd.Series(ys).rank(method="average").to_list()
    return _pearson(sx, sy)


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 2:
        return None
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    deny = math.sqrt(sum((y - my) ** 2 for y in ys))
    if denx == 0 or deny == 0:
        return None
    return num / (denx * deny)


def _group_key(row_or_tuple) -> tuple:
    return tuple(row_or_tuple)


def _groups(df: pd.DataFrame) -> dict[tuple, pd.DataFrame]:
    return {tuple(k if isinstance(k, tuple) else (k,)): g for k, g in df.groupby(GROUP_COLS, dropna=False)}


def illegal_moves_for_group(group: pd.DataFrame) -> list[str]:
    if group.empty or "fen" not in group.columns:
        return []
    fen = str(group["fen"].iloc[0])
    try:
        board = chess.Board(fen if len(fen.split()) == 6 else fen + " 0 1")
    except Exception:
        return sorted(set(group["move_uci"].astype(str)))
    legal = {m.uci() for m in board.legal_moves}
    return sorted(set(group.loc[~group["move_uci"].astype(str).isin(legal), "move_uci"].astype(str)))


def compare_profiles(left: pd.DataFrame, right: pd.DataFrame) -> ComparisonResult:
    required = set(GROUP_COLS + ["rank", "move_uci", "policy_probability", "fen"])
    for name, df in (("left", left), ("right", right)):
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"{name} CSV missing columns: {sorted(missing)}")
    left_groups = _groups(left)
    right_groups = _groups(right)
    all_keys = sorted(set(left_groups) | set(right_groups))
    rows = []
    top1_agree = []
    top3_agree = []
    corrs = []
    abs_means = []
    max_diffs = []
    for key in all_keys:
        lg = _ranked(left_groups.get(key, pd.DataFrame(columns=left.columns)))
        rg = _ranked(right_groups.get(key, pd.DataFrame(columns=right.columns)))
        missing_side = ""
        if lg.empty:
            missing_side = "left"
        elif rg.empty:
            missing_side = "right"
        left_top = lg["move_uci"].astype(str).tolist()
        right_top = rg["move_uci"].astype(str).tolist()
        left_top1 = left_top[0] if left_top else ""
        right_top1 = right_top[0] if right_top else ""
        t1 = bool(left_top1 and left_top1 == right_top1)
        t3 = bool(set(left_top[:3]) & set(right_top[:3])) if left_top and right_top else False
        inter10 = len(set(left_top[:10]) & set(right_top[:10]))
        fen_mismatch = False
        if not lg.empty and not rg.empty:
            fen_mismatch = fen4(str(lg["fen"].iloc[0])) != fen4(str(rg["fen"].iloc[0]))
        merged = pd.merge(
            lg[["move_uci", "policy_probability"]],
            rg[["move_uci", "policy_probability"]],
            on="move_uci",
            how="inner",
            suffixes=("_left", "_right"),
        )
        corr = None
        mean_abs = None
        max_abs = None
        if not merged.empty:
            lp = merged["policy_probability_left"].astype(float).tolist()
            rp = merged["policy_probability_right"].astype(float).tolist()
            corr = _pearson(lp, rp)
            diffs = [abs(a - b) for a, b in zip(lp, rp)]
            mean_abs = sum(diffs) / len(diffs)
            max_abs = max(diffs)
        if not missing_side:
            top1_agree.append(t1)
            top3_agree.append(t3)
            if corr is not None:
                corrs.append(corr)
            if mean_abs is not None:
                abs_means.append(mean_abs)
            if max_abs is not None:
                max_diffs.append(max_abs)
        illegal = sorted(set(illegal_moves_for_group(lg)) | set(illegal_moves_for_group(rg)))
        rows.append({
            "line_id": key[0],
            "elo": key[1],
            "missing_side": missing_side,
            "top1_left": left_top1,
            "top1_right": right_top1,
            "top1_agreement": t1,
            "top3_overlap": t3,
            "top10_intersection": inter10,
            "probability_correlation": corr,
            "mean_absolute_difference": mean_abs,
            "max_absolute_difference": max_abs,
            "top1_changed": bool(left_top1 and right_top1 and left_top1 != right_top1),
            "illegal_moves": " ".join(illegal),
            "fen_mismatch": fen_mismatch,
        })
    details = pd.DataFrame(rows)
    summary = {
        "groups_left": len(left_groups),
        "groups_right": len(right_groups),
        "groups_compared": int((details["missing_side"] == "").sum()) if not details.empty else 0,
        "missing_groups": int((details["missing_side"] != "").sum()) if not details.empty else 0,
        "top1_agreement_rate": sum(top1_agree) / len(top1_agree) if top1_agree else None,
        "top3_agreement_rate": sum(top3_agree) / len(top3_agree) if top3_agree else None,
        "mean_top10_intersection": float(details.loc[details["missing_side"] == "", "top10_intersection"].mean()) if not details.empty else None,
        "mean_probability_correlation": sum(corrs) / len(corrs) if corrs else None,
        "mean_absolute_difference": sum(abs_means) / len(abs_means) if abs_means else None,
        "max_absolute_difference": max(max_diffs) if max_diffs else None,
        "top1_changes": int(details["top1_changed"].sum()) if not details.empty else 0,
        "illegal_move_groups": int(details["illegal_moves"].astype(bool).sum()) if not details.empty else 0,
        "fen_mismatches": int(details["fen_mismatch"].sum()) if not details.empty else 0,
    }
    return ComparisonResult(details=details, summary=summary)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two Maia profile CSVs independently of row order.")
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()
    result = compare_profiles(pd.read_csv(args.left), pd.read_csv(args.right))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.details.to_csv(args.output, index=False)
    summary_path = args.summary or args.output.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(result.summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result.summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
