from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

ELOS = [1100, 1300, 1500, 1700, 1900, 2100]


def _top_moves(df: pd.DataFrame, n: int) -> list[str]:
    return df.sort_values(["rank", "move_uci"], kind="stable")["move_uci"].astype(str).head(n).tolist()


def _weighted_average(rows: list[dict], value: str, weight: str = "lichess_total") -> float | None:
    den = sum(float(r.get(weight, 0) or 0) for r in rows)
    if den <= 0:
        vals = [float(r[value]) for r in rows if pd.notna(r.get(value))]
        return sum(vals) / len(vals) if vals else None
    return sum(float(r.get(value, 0) or 0) * float(r.get(weight, 0) or 0) for r in rows) / den


def _summarize_subset(rows: list[dict]) -> dict:
    if not rows:
        return {
            "groups": 0,
            "maia_mass_covered_by_lichess": None,
            "top1_agreement_rate": None,
            "top3_agreement_rate": None,
            "lichess_outside_maia_top10_but_in_full_policy": 0,
            "remaining_divergences": 0,
        }
    return {
        "groups": len(rows),
        "maia_mass_covered_by_lichess": _weighted_average(rows, "maia_mass_covered_by_lichess"),
        "top1_agreement_rate": sum(bool(r["top1_agreement"]) for r in rows) / len(rows),
        "top3_agreement_rate": sum(bool(r["top3_agreement"]) for r in rows) / len(rows),
        "lichess_outside_maia_top10_but_in_full_policy": int(sum(int(r["lichess_outside_maia_top10_but_in_full_policy"]) for r in rows)),
        "remaining_divergences": int(sum(int(r["remaining_divergences"]) for r in rows)),
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
    rows: list[dict] = []
    for line_id in manifest_ids:
        for elo in ELOS:
            mg = maia[(maia["line_id"] == line_id) & (maia["elo"] == elo)].copy()
            lg = lichess[(lichess["line_id"] == line_id) & (lichess["elo_min"] == elo)].copy()
            if mg.empty and lg.empty:
                rows.append({
                    "line_id": line_id, "elo": elo, "speed": "ALL", "missing_side": "both",
                    "maia_mass_covered_by_lichess": 0.0, "lichess_total": 0,
                    "top1_agreement": False, "top3_agreement": False,
                    "lichess_outside_maia_top10_but_in_full_policy": 0,
                    "remaining_divergences": 1,
                })
                continue
            for speed in sorted(set(lg["speed"].astype(str))) or ["ALL"]:
                sg = lg[lg["speed"].astype(str) == speed] if speed != "ALL" else lg
                maia_probs = dict(zip(mg["move_uci"].astype(str), mg["policy_probability"].astype(float)))
                full_policy = set(maia_probs)
                maia_top1 = _top_moves(mg, 1)[0] if not mg.empty else ""
                maia_top3 = set(_top_moves(mg, 3))
                maia_top10 = set(_top_moves(mg, 10))
                if not sg.empty:
                    lichess_agg = sg.groupby("move_uci", as_index=False).agg({"count":"sum", "total_positions":"max", "frequency":"sum"})
                    lichess_top = lichess_agg.sort_values(["count", "frequency", "move_uci"], ascending=[False, False, True], kind="stable")
                    lichess_top1 = str(lichess_top["move_uci"].iloc[0])
                    lichess_top3 = set(lichess_top["move_uci"].astype(str).head(3))
                    lichess_moves = set(lichess_agg["move_uci"].astype(str))
                    total = int(lichess_agg["total_positions"].max()) if len(lichess_agg) else 0
                else:
                    lichess_top1 = ""
                    lichess_top3 = set()
                    lichess_moves = set()
                    total = 0
                covered_moves = full_policy & lichess_moves
                covered_mass = sum(maia_probs[m] for m in covered_moves)
                outside_top10_in_full = sorted((lichess_moves - maia_top10) & full_policy)
                top1_agree = bool(maia_top1 and lichess_top1 and maia_top1 == lichess_top1)
                top3_agree = bool(maia_top3 & lichess_top3)
                rows.append({
                    "line_id": line_id,
                    "elo": elo,
                    "speed": speed,
                    "missing_side": "maia" if mg.empty else ("lichess" if sg.empty else ""),
                    "maia_moves": len(full_policy),
                    "lichess_moves": len(lichess_moves),
                    "lichess_total": total,
                    "maia_mass_covered_by_lichess": covered_mass,
                    "maia_top1": maia_top1,
                    "lichess_top1": lichess_top1,
                    "top1_agreement": top1_agree,
                    "top3_agreement": top3_agree,
                    "lichess_outside_maia_top10_but_in_full_policy": len(outside_top10_in_full),
                    "outside_top10_moves": " ".join(outside_top10_in_full),
                    "remaining_divergences": int(not top1_agree),
                })
    detail = pd.DataFrame(rows)
    group_rows = []
    for (line_id, elo), g in detail.groupby(["line_id", "elo"]):
        row = g.iloc[0].to_dict()
        mg = maia[(maia["line_id"] == str(line_id)) & (maia["elo"] == int(elo))].copy()
        lg = lichess[(lichess["line_id"] == str(line_id)) & (lichess["elo_min"] == int(elo))].copy()
        maia_probs = dict(zip(mg["move_uci"].astype(str), mg["policy_probability"].astype(float)))
        lichess_moves = set(lg["move_uci"].astype(str))
        maia_top1 = _top_moves(mg, 1)[0] if not mg.empty else ""
        maia_top3 = set(_top_moves(mg, 3))
        if not lg.empty:
            lichess_agg = lg.groupby("move_uci", as_index=False).agg({"count":"sum", "frequency":"sum", "total_positions":"max"})
            lichess_top = lichess_agg.sort_values(["count", "frequency", "move_uci"], ascending=[False, False, True], kind="stable")
            lichess_top1 = str(lichess_top["move_uci"].iloc[0])
            lichess_top3 = set(lichess_top["move_uci"].astype(str).head(3))
        else:
            lichess_top1 = ""
            lichess_top3 = set()
        row["speed"] = "ALL"
        row["lichess_total"] = int(g["lichess_total"].sum())
        row["maia_mass_covered_by_lichess"] = float(sum(maia_probs[m] for m in (set(maia_probs) & lichess_moves)))
        row["top1_agreement"] = bool(maia_top1 and lichess_top1 and maia_top1 == lichess_top1)
        row["top3_agreement"] = bool(maia_top3 & lichess_top3)
        row["lichess_outside_maia_top10_but_in_full_policy"] = int(g["lichess_outside_maia_top10_but_in_full_policy"].sum())
        row["remaining_divergences"] = int(not row["top1_agreement"])
        group_rows.append(row)
    expected = len(manifest_ids) * len(ELOS)
    summary_rows = group_rows
    summary = {
        "expected_maia_groups": expected,
        "maia_groups_observed": int(maia.groupby(["line_id", "elo"]).ngroups),
        "detail_rows": len(detail),
        "overall_maia_mass_covered_by_lichess": _weighted_average(summary_rows, "maia_mass_covered_by_lichess"),
        "overall_top1_agreement_rate": sum(bool(r["top1_agreement"]) for r in summary_rows) / len(summary_rows) if summary_rows else None,
        "overall_top3_agreement_rate": sum(bool(r["top3_agreement"]) for r in summary_rows) / len(summary_rows) if summary_rows else None,
        "lichess_outside_maia_top10_but_in_full_policy": int(sum(int(r["lichess_outside_maia_top10_but_in_full_policy"]) for r in summary_rows)),
        "remaining_divergences": int(sum(int(r["remaining_divergences"]) for r in summary_rows)),
        "by_elo": {},
        "by_speed": {},
    }
    for elo, rows in pd.DataFrame(summary_rows).groupby("elo"):
        summary["by_elo"][str(int(elo))] = _summarize_subset(rows.to_dict("records"))
    for speed, rows in detail.groupby("speed"):
        if speed != "ALL":
            summary["by_speed"][str(speed)] = _summarize_subset(rows.to_dict("records"))
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
