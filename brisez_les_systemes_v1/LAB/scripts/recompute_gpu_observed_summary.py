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

    maia_groups_total = int(df[["line_id", "elo"]].drop_duplicates().shape[0])
    detail_rows = int(len(df))
    model_only = df[df["elo"].astype(int) == 2100].copy()
    missing_lichess = df[df["lichess_total"].fillna(0).astype(int) <= 0].copy()
    observed = df[df["lichess_total"].fillna(0).astype(int) > 0].copy()
    # Explicitly guard the historical bug: aggregate missing Lichess rows (speed=ALL,
    # missing_side=lichess) are model-only/missing evidence, not disagreements.
    observed = observed[~((observed["speed"].astype(str) == "ALL") & (observed["missing_side"].astype(str) == "lichess"))]

    observed_n = int(len(observed))
    summary = {
        "source_csv": str(csv_path),
        "maia_groups_total": maia_groups_total,
        "detail_rows": detail_rows,
        "lichess_observed_groups": observed_n,
        "lichess_missing_groups": int(len(missing_lichess)),
        "model_only_groups": int(len(model_only)),
        "model_only_status": "MODEL_ONLY_NO_MATCHING_LICHESS_BAND",
        "top1_agreement_observed_only": (bool_sum(observed["top1_agreement"]) / observed_n) if observed_n else None,
        "top3_agreement_observed_only": (bool_sum(observed["top3_agreement"]) / observed_n) if observed_n else None,
        "maia_mass_covered_observed_only": float(observed["maia_mass_covered_by_lichess"].mean()) if observed_n else None,
        "true_disagreements_observed_only": int(((~observed["top3_agreement"].fillna(False).astype(bool)) & (observed["lichess_total"].astype(int) > 0)).sum()),
        "excluded_from_agreement_rates": {
            "missing_side_lichess_speed_ALL_groups": int(((df["speed"].astype(str) == "ALL") & (df["missing_side"].astype(str) == "lichess")).sum()),
            "elo_2100_model_only_groups": int(len(model_only)),
        },
        "by_elo_observed_only": {},
        "by_speed_observed_only": {},
    }
    for elo, group in observed.groupby("elo"):
        n = int(len(group))
        summary["by_elo_observed_only"][str(int(elo))] = {
            "lichess_observed_groups": n,
            "top1_agreement_observed_only": bool_sum(group["top1_agreement"]) / n if n else None,
            "top3_agreement_observed_only": bool_sum(group["top3_agreement"]) / n if n else None,
            "maia_mass_covered_observed_only": float(group["maia_mass_covered_by_lichess"].mean()) if n else None,
            "true_disagreements_observed_only": int((~group["top3_agreement"].fillna(False).astype(bool)).sum()),
        }
    # Preserve 2100 explicitly as model-only even though it has no observed groups.
    summary["by_elo_observed_only"]["2100"] = {
        "status": "MODEL_ONLY_NO_MATCHING_LICHESS_BAND",
        "lichess_observed_groups": 0,
        "top1_agreement_observed_only": None,
        "top3_agreement_observed_only": None,
        "maia_mass_covered_observed_only": None,
        "true_disagreements_observed_only": 0,
    }
    for speed, group in observed.groupby("speed"):
        n = int(len(group))
        summary["by_speed_observed_only"][str(speed)] = {
            "lichess_observed_groups": n,
            "top1_agreement_observed_only": bool_sum(group["top1_agreement"]) / n if n else None,
            "top3_agreement_observed_only": bool_sum(group["top3_agreement"]) / n if n else None,
            "maia_mass_covered_observed_only": float(group["maia_mass_covered_by_lichess"].mean()) if n else None,
            "true_disagreements_observed_only": int((~group["top3_agreement"].fillna(False).astype(bool)).sum()),
        }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Recompute Maia full-policy vs Lichess summary on observed Lichess groups only.")
    parser.add_argument("--csv", type=Path, default=Path("DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess.csv"))
    parser.add_argument("--output", type=Path, default=Path("DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess_summary.json"))
    args = parser.parse_args()
    summary = summarize(args.csv)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {args.output}: observed={summary['lichess_observed_groups']} top3={summary['top3_agreement_observed_only']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
