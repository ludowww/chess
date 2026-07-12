from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

ELOS = [1100, 1300, 1500, 1700, 1900, 2100]
OBSERVED = "OBSERVED"
NO_LICHESS_DATA = "NO_LICHESS_DATA"
MODEL_ONLY_NO_MATCHING_LICHESS_BAND = "MODEL_ONLY_NO_MATCHING_LICHESS_BAND"
MISSING_MAIA = "MISSING_MAIA"


def _top_moves(df: pd.DataFrame, n: int) -> list[str]:
    if df.empty:
        return []
    return df.sort_values(["rank", "move_uci"], kind="stable")["move_uci"].astype(str).head(n).tolist()


def _safe_rate(num: int | float, den: int | float) -> float | None:
    return (num / den) if den else None


def _weighted_average(rows: list[dict], value: str, weight: str = "lichess_total") -> float | None:
    den = sum(float(r.get(weight, 0) or 0) for r in rows)
    if den <= 0:
        vals = [float(r[value]) for r in rows if pd.notna(r.get(value))]
        return sum(vals) / len(vals) if vals else None
    return sum(float(r.get(value, 0) or 0) * float(r.get(weight, 0) or 0) for r in rows) / den


def _observed(rows: list[dict]) -> list[dict]:
    return [r for r in rows if int(r.get("lichess_total", 0) or 0) > 0]


def _summarize_subset(rows: list[dict], *, include_speed_counts: bool = False) -> dict:
    observed = _observed(rows)
    true_disagreements = sum(1 for r in observed if r.get("top1_agreement") is False)
    summary = {
        "groups": len(rows),
        "observed_groups": len(observed),
        "maia_mass_covered_by_lichess": _weighted_average(observed, "maia_mass_covered_by_lichess"),
        "top1_agreement_rate": _safe_rate(sum(1 for r in observed if r.get("top1_agreement") is True), len(observed)),
        "top3_agreement_rate": _safe_rate(sum(1 for r in observed if r.get("top3_agreement") is True), len(observed)),
        "lichess_outside_maia_top10_but_in_full_policy": int(sum(int(r.get("lichess_outside_maia_top10_but_in_full_policy", 0) or 0) for r in observed)),
        "remaining_divergences": int(true_disagreements),
    }
    if include_speed_counts:
        summary["unique_rows"] = len({str(r.get("line_id")) for r in observed})
        summary["total_positions"] = int(sum(int(r.get("lichess_total", 0) or 0) for r in observed))
    return summary


def _lichess_aggregate(df: pd.DataFrame) -> tuple[str, set[str], int, pd.DataFrame]:
    if df.empty:
        return "", set(), 0, pd.DataFrame(columns=["move_uci", "count", "frequency", "total_positions"])
    agg = df.groupby("move_uci", as_index=False).agg({"count": "sum", "frequency": "sum", "total_positions": "max"})
    top = agg.sort_values(["count", "frequency", "move_uci"], ascending=[False, False, True], kind="stable")
    return str(top["move_uci"].iloc[0]), set(top["move_uci"].astype(str).head(3)), int(agg["total_positions"].max()), agg


def _status(mg: pd.DataFrame, lg: pd.DataFrame, elo: int, lichess_bands: set[int]) -> str:
    if mg.empty:
        return MISSING_MAIA
    if elo not in lichess_bands:
        return MODEL_ONLY_NO_MATCHING_LICHESS_BAND
    if lg.empty or int(lg["total_positions"].max()) <= 0:
        return NO_LICHESS_DATA
    return OBSERVED


def _build_row(line_id: str, elo: int, speed: str, mg: pd.DataFrame, lg: pd.DataFrame, status: str) -> dict:
    maia_probs = dict(zip(mg["move_uci"].astype(str), mg["policy_probability"].astype(float)))
    full_policy = set(maia_probs)
    maia_top1 = _top_moves(mg, 1)[0] if not mg.empty else ""
    maia_top3 = set(_top_moves(mg, 3))
    maia_top10 = set(_top_moves(mg, 10))
    lichess_top1, lichess_top3, total, lichess_agg = _lichess_aggregate(lg if status == OBSERVED else lg.iloc[0:0])
    lichess_moves = set(lichess_agg["move_uci"].astype(str)) if not lichess_agg.empty else set()
    covered_moves = full_policy & lichess_moves
    outside_top10_in_full = sorted((lichess_moves - maia_top10) & full_policy)
    if status == OBSERVED:
        top1_agree = bool(maia_top1 and lichess_top1 and maia_top1 == lichess_top1)
        top3_agree = bool(maia_top3 & lichess_top3)
        remaining = int(not top1_agree)
        covered_mass: float | None = float(sum(maia_probs[m] for m in covered_moves))
    else:
        top1_agree = None
        top3_agree = None
        remaining = 0
        covered_mass = None
    return {
        "line_id": line_id,
        "elo": elo,
        "speed": speed,
        "comparison_status": status,
        "missing_side": "maia" if status == MISSING_MAIA else ("lichess" if status == NO_LICHESS_DATA else ""),
        "maia_moves": len(full_policy),
        "lichess_moves": len(lichess_moves),
        "lichess_total": total if status == OBSERVED else 0,
        "maia_mass_covered_by_lichess": covered_mass,
        "maia_top1": maia_top1,
        "lichess_top1": lichess_top1,
        "top1_agreement": top1_agree,
        "top3_agreement": top3_agree,
        "lichess_outside_maia_top10_but_in_full_policy": len(outside_top10_in_full) if status == OBSERVED else 0,
        "outside_top10_moves": " ".join(outside_top10_in_full),
        "remaining_divergences": remaining,
    }


def compare_full_policy_to_lichess(maia: pd.DataFrame, lichess: pd.DataFrame, manifest: pd.DataFrame | None = None) -> tuple[pd.DataFrame, dict]:
    required_maia = {"line_id", "elo", "rank", "move_uci", "policy_probability"}
    required_lichess = {"line_id", "elo_min", "speed", "move_uci", "count", "total_positions", "frequency"}
    if missing := required_maia - set(maia.columns):
        raise ValueError(f"Maia CSV missing columns: {sorted(missing)}")
    if missing := required_lichess - set(lichess.columns):
        raise ValueError(f"Lichess CSV missing columns: {sorted(missing)}")
    if "position_role" in lichess.columns:
        lichess = lichess[lichess["position_role"] == "after_key"].copy()
    manifest_ids = sorted(set(manifest["line_id"].astype(str))) if manifest is not None else sorted(set(maia["line_id"].astype(str)))
    maia = maia.copy()
    lichess = lichess.copy()
    maia["line_id"] = maia["line_id"].astype(str)
    lichess["line_id"] = lichess["line_id"].astype(str)
    maia["elo"] = maia["elo"].astype(int)
    lichess["elo_min"] = lichess["elo_min"].astype(int)
    lichess_bands = set(lichess["elo_min"].astype(int))

    detail_rows: list[dict] = []
    group_rows: list[dict] = []
    for line_id in manifest_ids:
        for elo in ELOS:
            mg = maia[(maia["line_id"] == line_id) & (maia["elo"] == elo)].copy()
            lg = lichess[(lichess["line_id"] == line_id) & (lichess["elo_min"] == elo)].copy()
            if mg.empty and lg.empty and manifest is None:
                continue
            status = _status(mg, lg, elo, lichess_bands)
            speeds = sorted(set(lg["speed"].astype(str))) if status == OBSERVED else ["ALL"]
            for speed in speeds:
                sg = lg[lg["speed"].astype(str) == speed] if speed != "ALL" else lg
                detail_rows.append(_build_row(line_id, elo, speed, mg, sg, status))
            group_rows.append(_build_row(line_id, elo, "ALL", mg, lg, status))

    detail = pd.DataFrame(detail_rows)
    maia_groups_total = int(maia.groupby(["line_id", "elo"]).ngroups)
    observed_rows = _observed(group_rows)
    missing_groups = [r for r in group_rows if r.get("comparison_status") == NO_LICHESS_DATA]
    model_only_groups = [r for r in group_rows if r.get("comparison_status") == MODEL_ONLY_NO_MATCHING_LICHESS_BAND]
    summary = {
        "expected_maia_groups": len(manifest_ids) * len(ELOS),
        "maia_groups_observed": maia_groups_total,
        "maia_groups_total": maia_groups_total,
        "lichess_observed_groups": len(observed_rows),
        "lichess_missing_groups": len(missing_groups),
        "model_only_groups": len(model_only_groups),
        "detail_rows": len(detail),
        "overall_maia_mass_covered_by_lichess": _weighted_average(observed_rows, "maia_mass_covered_by_lichess"),
        "overall_top1_agreement_rate": _safe_rate(sum(1 for r in observed_rows if r.get("top1_agreement") is True), len(observed_rows)),
        "overall_top3_agreement_rate": _safe_rate(sum(1 for r in observed_rows if r.get("top3_agreement") is True), len(observed_rows)),
        "top1_agreement_observed_only": _safe_rate(sum(1 for r in observed_rows if r.get("top1_agreement") is True), len(observed_rows)),
        "top3_agreement_observed_only": _safe_rate(sum(1 for r in observed_rows if r.get("top3_agreement") is True), len(observed_rows)),
        "maia_mass_covered_observed_only": _weighted_average(observed_rows, "maia_mass_covered_by_lichess"),
        "true_disagreements_observed_only": int(sum(1 for r in observed_rows if r.get("top1_agreement") is False)),
        "lichess_outside_maia_top10_but_in_full_policy": int(sum(int(r.get("lichess_outside_maia_top10_but_in_full_policy", 0) or 0) for r in observed_rows)),
        "remaining_divergences": int(sum(1 for r in observed_rows if r.get("top1_agreement") is False)),
        "by_elo": {},
        "by_speed": {},
    }
    for elo, rows in pd.DataFrame(group_rows).groupby("elo"):
        summary["by_elo"][str(int(elo))] = _summarize_subset(rows.to_dict("records"))
    if not detail.empty:
        for speed, rows in detail[detail["speed"] != "ALL"].groupby("speed"):
            summary["by_speed"][str(speed)] = _summarize_subset(rows.to_dict("records"), include_speed_counts=True)
    return detail, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare Maia full legal policy GPU output with expanded Lichess response data.")
    parser.add_argument("--maia", type=Path, default=Path("DATA/maia3_79m_full_policy_gpu.csv"))
    parser.add_argument("--lichess", type=Path, default=Path("DATA/lichess_test_expanded.csv"))
    parser.add_argument("--manifest", type=Path, default=Path("DATA/core_40_index.csv"))
    parser.add_argument("--output", type=Path, default=Path("DATA/maia3_full_policy_gpu_vs_lichess.csv"))
    parser.add_argument("--summary", type=Path, default=Path("DATA/maia3_full_policy_gpu_vs_lichess_summary.json"))
    args = parser.parse_args()
    manifest = pd.read_csv(args.manifest)
    detail, summary = compare_full_policy_to_lichess(pd.read_csv(args.maia), pd.read_csv(args.lichess), manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    detail.to_csv(args.output, index=False)
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
