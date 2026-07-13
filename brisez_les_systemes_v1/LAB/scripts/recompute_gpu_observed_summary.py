from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def bool_sum(series: pd.Series) -> int:
    return int(series.fillna(False).astype(bool).sum())


def summarize(csv_path: Path) -> dict:
    df = pd.read_csv(csv_path)
    required = {"line_id", "elo", "speed", "missing_side", "lichess_total", "top1_agreement", "top3_agreement", "maia_mass_covered_by_lichess", "remaining_divergences"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in {csv_path}: {sorted(missing)}")

    maia_group_cols = ["line_id", "elo"]
    maia_groups = df[maia_group_cols].drop_duplicates()
    maia_groups_total = int(len(maia_groups))
    detail_rows = int(len(df))

    observed_speed = df[df["lichess_total"].fillna(0).astype(int) > 0].copy()
    # Historical guard: rows synthesized as speed=ALL/missing_side=lichess are
    # missing-evidence Maia groups, not Lichess observations or disagreements.
    observed_speed = observed_speed[
        ~((observed_speed["speed"].astype(str) == "ALL") & (observed_speed["missing_side"].astype(str) == "lichess"))
    ]
    observed_speed_n = int(len(observed_speed))

    observed_maia_groups = observed_speed[maia_group_cols].drop_duplicates()
    lichess_observed_maia_groups = int(len(observed_maia_groups))
    lichess_missing_maia_groups = int(maia_groups_total - lichess_observed_maia_groups)

    model_only_maia_groups = int(df.loc[df["elo"].astype(int) == 2100, maia_group_cols].drop_duplicates().shape[0])
    model_only_keys = set(map(tuple, df.loc[df["elo"].astype(int) == 2100, maia_group_cols].drop_duplicates().to_records(index=False)))
    missing_keys = set(map(tuple, maia_groups.to_records(index=False))) - set(map(tuple, observed_maia_groups.to_records(index=False)))
    if not model_only_keys <= missing_keys:
        raise AssertionError("Elo 2100 model-only groups must be a subset of missing Lichess Maia groups")
    if lichess_observed_maia_groups + lichess_missing_maia_groups != maia_groups_total:
        raise AssertionError("Observed + missing Maia groups must equal total Maia groups")

    summary = {
        "source_csv": str(csv_path),
        "maia_groups_total": maia_groups_total,
        "detail_rows": detail_rows,
        "lichess_observed_maia_groups": lichess_observed_maia_groups,
        "lichess_missing_maia_groups": lichess_missing_maia_groups,
        "lichess_observed_speed_groups": observed_speed_n,
        "model_only_maia_groups": model_only_maia_groups,
        "model_only_status": "MODEL_ONLY_NO_MATCHING_LICHESS_BAND",
        "top1_agreement_observed_speed_groups": (bool_sum(observed_speed["top1_agreement"]) / observed_speed_n) if observed_speed_n else None,
        "top3_agreement_observed_speed_groups": (bool_sum(observed_speed["top3_agreement"]) / observed_speed_n) if observed_speed_n else None,
        "maia_mass_covered_observed_speed_groups_unweighted_mean": float(observed_speed["maia_mass_covered_by_lichess"].mean()) if observed_speed_n else None,
        "top3_disagreements_observed_speed_groups": int((~observed_speed["top3_agreement"].fillna(False).astype(bool)).sum()),
        "excluded_from_agreement_rates": {
            "missing_side_lichess_speed_ALL_rows": int(((df["speed"].astype(str) == "ALL") & (df["missing_side"].astype(str) == "lichess")).sum()),
            "elo_2100_model_only_maia_groups": model_only_maia_groups,
        },
        "by_elo_observed_speed_groups": {},
        "by_speed_observed_groups": {},
    }
    for elo, group in observed_speed.groupby("elo"):
        n = int(len(group))
        summary["by_elo_observed_speed_groups"][str(int(elo))] = {
            "lichess_observed_speed_groups": n,
            "lichess_observed_maia_groups": int(group[maia_group_cols].drop_duplicates().shape[0]),
            "top1_agreement_observed_speed_groups": bool_sum(group["top1_agreement"]) / n if n else None,
            "top3_agreement_observed_speed_groups": bool_sum(group["top3_agreement"]) / n if n else None,
            "maia_mass_covered_observed_speed_groups_unweighted_mean": float(group["maia_mass_covered_by_lichess"].mean()) if n else None,
            "top3_disagreements_observed_speed_groups": int((~group["top3_agreement"].fillna(False).astype(bool)).sum()),
        }
    summary["by_elo_observed_speed_groups"]["2100"] = {
        "status": "MODEL_ONLY_NO_MATCHING_LICHESS_BAND",
        "lichess_observed_speed_groups": 0,
        "lichess_observed_maia_groups": 0,
        "top1_agreement_observed_speed_groups": None,
        "top3_agreement_observed_speed_groups": None,
        "maia_mass_covered_observed_speed_groups_unweighted_mean": None,
        "top3_disagreements_observed_speed_groups": 0,
    }
    for speed, group in observed_speed.groupby("speed"):
        n = int(len(group))
        summary["by_speed_observed_groups"][str(speed)] = {
            "lichess_observed_speed_groups": n,
            "lichess_observed_maia_groups": int(group[maia_group_cols].drop_duplicates().shape[0]),
            "top1_agreement_observed_speed_groups": bool_sum(group["top1_agreement"]) / n if n else None,
            "top3_agreement_observed_speed_groups": bool_sum(group["top3_agreement"]) / n if n else None,
            "maia_mass_covered_observed_speed_groups_unweighted_mean": float(group["maia_mass_covered_by_lichess"].mean()) if n else None,
            "top3_disagreements_observed_speed_groups": int((~group["top3_agreement"].fillna(False).astype(bool)).sum()),
        }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Recompute Maia full-policy vs Lichess summary with explicit Maia-group and speed-cell denominators.")
    parser.add_argument("--csv", type=Path, default=Path("DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess.csv"))
    parser.add_argument("--output", type=Path, default=Path("DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess_summary.json"))
    args = parser.parse_args()
    summary = summarize(args.csv)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"wrote {args.output}: observed_maia={summary['lichess_observed_maia_groups']} "
        f"observed_speed={summary['lichess_observed_speed_groups']} "
        f"top3_speed={summary['top3_agreement_observed_speed_groups']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
