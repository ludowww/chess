from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd

from common import load_manifest


def normalized_entropy(values: pd.Series) -> float:
    probs = values[values > 0].to_numpy(dtype=float)
    if len(probs) <= 1:
        return 0.0
    probs = probs / probs.sum()
    return float(-(probs * np.log(probs)).sum() / math.log(len(probs)))


def weighted_error_rate(df: pd.DataFrame, threshold: int = 40) -> float:
    mass = df["frequency"].sum()
    if mass <= 0:
        return float("nan")
    return float((df["frequency"] * (df["response_loss_cp"] >= threshold)).sum() / mass)


def build_scorecards(
    manifest_path: Path,
    stockfish_path: Path | None,
    maia_evaluated_path: Path | None,
    lichess_distribution_path: Path | None,
    lichess_evaluated_path: Path | None,
) -> pd.DataFrame:
    manifest = load_manifest(manifest_path)
    out = manifest[["line_id","bias_code","title","key_move_uci","editorial_our_simplicity_1_5","editorial_learning_longevity_1_5"]].copy()
    out["our_playability_editorial_0_100"] = out["editorial_our_simplicity_1_5"] * 20
    out["learning_longevity_editorial_0_100"] = out["editorial_learning_longevity_1_5"] * 20
    evidence = pd.Series(20, index=out.index, dtype=int)  # manifest + editorial layer

    if stockfish_path and stockfish_path.exists():
        sf = pd.read_csv(stockfish_path)
        sf_agg = sf.groupby("line_id")["loss_for_black_cp"].max().rename("engine_max_loss_cp")
        out = out.merge(sf_agg, on="line_id", how="left")
        out["engine_safety_0_100"] = (100 - out["engine_max_loss_cp"].fillna(100) * 1.5).clip(0,100)
        evidence += out["engine_max_loss_cp"].notna().astype(int) * 25
    else:
        out["engine_max_loss_cp"] = np.nan
        out["engine_safety_0_100"] = np.nan

    if maia_evaluated_path and maia_evaluated_path.exists():
        maia = pd.read_csv(maia_evaluated_path)
        maia["frequency"] = maia.get("frequency", maia.get("policy_probability"))
        per_elo = maia.groupby(["line_id","elo"], dropna=False).apply(weighted_error_rate, include_groups=False).rename("error_rate").reset_index()
        maia_error = per_elo.groupby("line_id")["error_rate"].mean().mul(100).rename("maia_human_error_proxy_0_100")
        maia_robust = per_elo.groupby("line_id")["error_rate"].min().mul(100).rename("maia_cross_elo_floor_0_100")
        maia_entropy = (
            maia.groupby(["line_id","elo"], dropna=False)["frequency"]
            .apply(normalized_entropy)
            .groupby("line_id").mean().mul(100)
            .rename("maia_response_entropy_0_100")
        )
        out=out.merge(maia_error,on="line_id",how="left").merge(maia_robust,on="line_id",how="left").merge(maia_entropy,on="line_id",how="left")
        evidence += out["maia_human_error_proxy_0_100"].notna().astype(int)*20
    else:
        out["maia_human_error_proxy_0_100"] = np.nan
        out["maia_cross_elo_floor_0_100"] = np.nan
        out["maia_response_entropy_0_100"] = np.nan

    if lichess_distribution_path and lichess_distribution_path.exists():
        ld = pd.read_csv(lichess_distribution_path)
        before = ld[ld["position_role"] == "before_key"].merge(out[["line_id","key_move_uci"]], on="line_id", how="left")
        before["candidate_frequency"] = np.where(before["move_uci"] == before["key_move_uci"], before["frequency"], 0.0)
        surprise = (1 - before.groupby("line_id")["candidate_frequency"].sum().clip(0,1)).mul(100).rename("lichess_surprise_0_100")
        after = ld[ld["position_role"] == "after_key"]
        empirical_entropy = (
            after.groupby(["line_id","elo_min","speed","split"], dropna=False)["frequency"]
            .apply(normalized_entropy)
            .groupby("line_id").mean().mul(100)
            .rename("lichess_response_entropy_0_100")
        )
        sample = ld.groupby("line_id")["total_positions"].max().rename("empirical_max_position_sample")
        out=out.merge(surprise,on="line_id",how="left").merge(empirical_entropy,on="line_id",how="left").merge(sample,on="line_id",how="left")
        evidence += out["lichess_surprise_0_100"].notna().astype(int)*15
    else:
        out["lichess_surprise_0_100"] = np.nan
        out["lichess_response_entropy_0_100"] = np.nan
        out["empirical_max_position_sample"] = np.nan

    if lichess_evaluated_path and lichess_evaluated_path.exists():
        emp = pd.read_csv(lichess_evaluated_path)
        group_cols = [c for c in ["line_id","elo_min","speed","split"] if c in emp.columns]
        per_band = emp.groupby(group_cols, dropna=False).apply(weighted_error_rate, include_groups=False).rename("error_rate").reset_index()
        human_error = per_band.groupby("line_id")["error_rate"].mean().mul(100).rename("lichess_human_error_rate_0_100")
        cross_elo = per_band.groupby("line_id")["error_rate"].min().mul(100).rename("empirical_cross_elo_floor_0_100")
        out=out.merge(human_error,on="line_id",how="left").merge(cross_elo,on="line_id",how="left")
        evidence += out["lichess_human_error_rate_0_100"].notna().astype(int)*20
    else:
        out["lichess_human_error_rate_0_100"] = np.nan
        out["empirical_cross_elo_floor_0_100"] = np.nan

    out["evidence_completeness_0_100"] = evidence.clip(0,100)
    required = ["engine_safety_0_100","maia_human_error_proxy_0_100","lichess_surprise_0_100","lichess_human_error_rate_0_100"]
    complete = out[required].notna().all(axis=1)
    out["practical_edge_score_0_100"] = np.nan
    out.loc[complete,"practical_edge_score_0_100"] = (
        out.loc[complete,"engine_safety_0_100"]*0.25 +
        out.loc[complete,"maia_human_error_proxy_0_100"]*0.15 +
        out.loc[complete,"lichess_surprise_0_100"]*0.10 +
        out.loc[complete,"lichess_human_error_rate_0_100"]*0.25 +
        out.loc[complete,"our_playability_editorial_0_100"]*0.15 +
        out.loc[complete,"learning_longevity_editorial_0_100"]*0.10
    )
    out["promotion_status"] = np.where(
        out["evidence_completeness_0_100"] >= 80,
        "ELIGIBLE_FOR_EDITORIAL_REVIEW",
        "INSUFFICIENT_EVIDENCE",
    )
    return out


def main() -> int:
    parser=argparse.ArgumentParser(description="Create evidence-aware scorecards; absent evidence remains blank.")
    parser.add_argument("--manifest",required=True,type=Path)
    parser.add_argument("--stockfish",type=Path)
    parser.add_argument("--maia-evaluated",type=Path)
    parser.add_argument("--lichess-distribution",type=Path)
    parser.add_argument("--lichess-evaluated",type=Path)
    parser.add_argument("--output",required=True,type=Path)
    args=parser.parse_args()
    df=build_scorecards(args.manifest,args.stockfish,args.maia_evaluated,args.lichess_distribution,args.lichess_evaluated)
    df.to_csv(args.output,index=False)
    print(f"Wrote {len(df)} scorecards to {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
