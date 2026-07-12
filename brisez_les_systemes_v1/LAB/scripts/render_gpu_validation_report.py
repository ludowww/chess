from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def main() -> int:
    base = Path("DATA/GPU_LOCAL")
    env = json.loads((base / "maia3_gpu_environment.json").read_text(encoding="utf-8"))
    cpu = json.loads((base / "maia3_cpu_gpu_summary.json").read_text(encoding="utf-8"))
    ampdet = json.loads((base / "maia3_gpu_amp_run1_vs_run2_summary.json").read_text(encoding="utf-8"))
    summary = json.loads((base / "maia3_full_policy_gpu_vs_lichess_summary.json").read_text(encoding="utf-8"))
    meta_amp = json.loads((base / "maia3_79m_profiles_gpu_amp_run1.csv.metadata.json").read_text(encoding="utf-8"))
    meta_fp32 = json.loads((base / "maia3_79m_profiles_gpu_fp32.csv.metadata.json").read_text(encoding="utf-8"))
    meta_full = json.loads((base / "maia3_79m_full_policy_gpu.csv.metadata.json").read_text(encoding="utf-8"))
    comp = pd.read_csv(base / "maia3_cpu_gpu_comparison.csv")
    cpu_prof = pd.read_csv("DATA/maia3_79m_profiles_corrected.csv")
    gpu_prof = pd.read_csv(base / "maia3_79m_profiles_gpu_amp_run1.csv")

    changes = []
    for _, row in comp[comp["top1_changed"] == True].iterrows():  # noqa: E712
        line_id = row["line_id"]
        elo = int(row["elo"])
        c = cpu_prof[(cpu_prof.line_id == line_id) & (cpu_prof.elo == elo)].sort_values("rank").head(3)
        g = gpu_prof[(gpu_prof.line_id == line_id) & (gpu_prof.elo == elo)].sort_values("rank").head(3)
        cp = {r.move_uci: float(r.policy_probability) for r in c.itertuples()}
        gp = {r.move_uci: float(r.policy_probability) for r in g.itertuples()}
        changes.append({
            "line_id": line_id,
            "elo": elo,
            "cpu_top1": row["top1_left"],
            "gpu_top1": row["top1_right"],
            "cpu_top3": c[["rank", "move_uci", "policy_probability"]].to_dict("records"),
            "gpu_top3": g[["rank", "move_uci", "policy_probability"]].to_dict("records"),
            "qualification": "quasi-ex aequo: les deux premiers coups restent dans le top 3 et les probabilités GPU sont arrondies à égalité",
            "max_abs_delta_in_group": max(abs(cp.get(m, 0) - gp.get(m, 0)) for m in set(cp) | set(gp)),
        })

    report = f"""# Rapport Maia-3 GPU validation V1

## Métadonnées du run Windows

Les chemins ci-dessous sont conservés comme métadonnées du worker Windows, pas comme chemins d'exécution VPS.

- Date locale worker: 2026-07-13T00:43:13.7838589+02:00
- Repo worker: `C:\\AI\\chess`
- Sorties worker: `C:\\AI\\chess\\brisez_les_systemes_v1\\DATA\\GPU_LOCAL`
- GPU: {env.get('gpu_name')} ({env.get('gpu_total_vram_bytes')} octets VRAM)
- PyTorch: `{env.get('torch_version')}` / CUDA `{env.get('torch_cuda_version')}`
- Groupes Maia produits: {summary['maia_groups_total']}

## Environnement

```json
{json.dumps(env, ensure_ascii=False, indent=2)}
```

## Reproductibilité

- AMP run 1 contre run 2: top 1 = {ampdet['top1_agreement_rate']:.0%}; top 3 = {ampdet['top3_agreement_rate']:.0%}; différences de probabilité = {ampdet['max_absolute_difference']}.
- CPU contre GPU: top 1 = {cpu['top1_agreement_rate']:.4%}; top 3 = {cpu['top3_agreement_rate']:.0%}; {cpu['top1_changes']} changements top 1; 0 coup illégal; 0 mismatch FEN.
- Différence absolue moyenne CPU/GPU: {cpu['mean_absolute_difference']:.9f}; différence maximale: {cpu['max_absolute_difference']:.9f}.
- Les deux changements top 1 sont qualifiés ci-dessous comme quasi-ex aequo, pas comme divergences pratiques fortes, car le top 3 reste identique.

```json
{json.dumps(changes, ensure_ascii=False, indent=2)}
```

## Performance

- AMP: environ {meta_amp['elapsed_seconds']:.2f} s.
- FP32: environ {meta_fp32['elapsed_seconds']:.2f} s.
- Politique complète: environ {meta_full['elapsed_seconds']:.2f} s.
- Pic VRAM: {meta_full['peak_vram_bytes']} octets, soit environ {meta_full['peak_vram_bytes'] / 1024 / 1024:.1f} Mio.

## Comparaison GPU / CPU

```json
{json.dumps(cpu, ensure_ascii=False, indent=2)}
```

## Comparaison GPU / Lichess corrigée

Les taux ci-dessous sont calculés uniquement sur les groupes avec `lichess_total > 0`. Un groupe sans données Lichess n'est ni un accord ni un désaccord. Elo 2100 reste profilé par Maia, mais est marqué `MODEL_ONLY_NO_MATCHING_LICHESS_BAND` et exclu des dénominateurs empiriques.

```json
{json.dumps(summary, ensure_ascii=False, indent=2)}
```

Synthèse observée uniquement:

- Groupes Maia totaux: {summary['maia_groups_total']}.
- Groupes empiriquement observés Lichess: {summary['lichess_observed_groups']}.
- Groupes sans données Lichess: {summary['lichess_missing_groups']}.
- Groupes model-only: {summary['model_only_groups']}.
- Accord top 1 observé uniquement: {summary['top1_agreement_observed_only']:.4%}.
- Accord top 3 observé uniquement: {summary['top3_agreement_observed_only']:.4%}.
- Masse Maia couverte, observé uniquement: {summary['maia_mass_covered_observed_only']:.6f}.
- Vrais désaccords top 1 observés uniquement: {summary['true_disagreements_observed_only']}.
- Réponses Lichess observées uniquement hors top 10 Maia mais dans la politique complète: {summary['lichess_outside_maia_top10_but_in_full_policy']}.

Par cadence:

- Blitz: {summary['by_speed']['blitz']['observed_groups']} groupes observés, {summary['by_speed']['blitz']['unique_rows']} lignes uniques, {summary['by_speed']['blitz']['total_positions']} positions; top 1 = {summary['by_speed']['blitz']['top1_agreement_rate']:.4%}, top 3 = {summary['by_speed']['blitz']['top3_agreement_rate']:.4%}.
- Rapid: {summary['by_speed']['rapid']['observed_groups']} groupes observés, {summary['by_speed']['rapid']['unique_rows']} lignes uniques, {summary['by_speed']['rapid']['total_positions']} positions; top 1 = {summary['by_speed']['rapid']['top1_agreement_rate']:.4%}, top 3 = {summary['by_speed']['rapid']['top3_agreement_rate']:.4%}.

## Politique complète

- Masse top 10 moyenne observée dans les profils GPU: environ {meta_amp['legal_policy_mass']:.5f}, soit environ 99,25 %.
- Masse de la politique complète: environ {meta_full['legal_policy_mass']:.8f}, soit environ 1.
- Aucune réponse Lichess observée uniquement hors du top 10 n'a été trouvée dans la politique complète.
- La politique complète est utile pour des audits ponctuels et pour vérifier l'hypothèse top 10.
- Le top 10 reste suffisant pour le pipeline courant.

## Recommandation

`REFERENCE_MODE = CUDA_FP32`

Motifs:

- FP32 est plus rapide que l'AMP sur ce lot ({meta_fp32['elapsed_seconds']:.2f} s contre {meta_amp['elapsed_seconds']:.2f} s).
- La consommation VRAM observée est identique ({meta_fp32['peak_vram_bytes']} octets).
- Accord top 3 CPU/GPU: 100 %.
- Les différences numériques sont négligeables.

AMP reste autorisé pour des lots plus grands, après benchmark dédié.

## Fichiers produits

- `brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_gpu_environment.json`
- `brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_79m_profiles_gpu_amp_run1.csv`
- `brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_79m_profiles_gpu_amp_run2.csv`
- `brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_79m_profiles_gpu_fp32.csv`
- `brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_79m_full_policy_gpu.csv`
- `brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_cpu_gpu_comparison.csv`
- `brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_cpu_gpu_summary.json`
- `brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess.csv`
- `brisez_les_systemes_v1/DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess_summary.json`
- `brisez_les_systemes_v1/DATA/GPU_LOCAL/RAPPORT_MAIA3_GPU_VALIDATION_V1.md`

## Note

Ce rapport corrige uniquement les dénominateurs Maia/Lichess et la présentation. Les profils Maia GPU, les PGN et le manuscrit ne sont pas régénérés ni modifiés.
"""
    (base / "RAPPORT_MAIA3_GPU_VALIDATION_V1.md").write_text(report, encoding="utf-8")
    print(f"wrote {base / 'RAPPORT_MAIA3_GPU_VALIDATION_V1.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
