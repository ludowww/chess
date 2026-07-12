# Rapport Maia-3 GPU validation V1

## Métadonnées du run Windows

Les chemins ci-dessous sont conservés comme métadonnées du worker Windows, pas comme chemins d'exécution VPS.

- Date locale worker: 2026-07-13T00:43:13.7838589+02:00
- Repo worker: `C:\AI\chess`
- Sorties worker: `C:\AI\chess\brisez_les_systemes_v1\DATA\GPU_LOCAL`
- GPU: NVIDIA GeForce RTX 3090 (25769279488 octets VRAM)
- PyTorch: `2.11.0+cu128` / CUDA `12.8`
- Groupes Maia produits: 240

## Environnement

```json
{
  "python_version": "3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]",
  "python_executable": "C:\\AI\\chess\\.venv-gpu\\Scripts\\python.exe",
  "platform": "Windows-10-10.0.26200-SP0",
  "torch_version": "2.11.0+cu128",
  "torch_cuda_version": "12.8",
  "cuda_available": true,
  "gpu_name": "NVIDIA GeForce RTX 3090",
  "gpu_total_vram_bytes": 25769279488,
  "device_capability": [
    8,
    6
  ]
}
```

## Reproductibilité

- AMP run 1 contre run 2: top 1 = 100%; top 3 = 100%; différences de probabilité = 0.0.
- CPU contre GPU: top 1 = 99.1667%; top 3 = 100%; 2 changements top 1; 0 coup illégal; 0 mismatch FEN.
- Différence absolue moyenne CPU/GPU: 0.000364368; différence maximale: 0.005118191.
- Les deux changements top 1 sont qualifiés ci-dessous comme quasi-ex aequo, pas comme divergences pratiques fortes, car le top 3 reste identique.

```json
[
  {
    "line_id": "LON-02",
    "elo": 1300,
    "cpu_top1": "c2c1",
    "gpu_top1": "c2d2",
    "cpu_top3": [
      {
        "rank": 1,
        "move_uci": "c2c1",
        "policy_probability": 0.3170020878314972
      },
      {
        "rank": 2,
        "move_uci": "c2d2",
        "policy_probability": 0.3150431215763092
      },
      {
        "rank": 3,
        "move_uci": "c2f5",
        "policy_probability": 0.2948450744152069
      }
    ],
    "gpu_top3": [
      {
        "rank": 1,
        "move_uci": "c2d2",
        "policy_probability": 0.3155406713485718
      },
      {
        "rank": 2,
        "move_uci": "c2c1",
        "policy_probability": 0.3155406713485718
      },
      {
        "rank": 3,
        "move_uci": "c2f5",
        "policy_probability": 0.2964230477809906
      }
    ],
    "qualification": "quasi-ex aequo: les deux premiers coups restent dans le top 3 et les probabilités GPU sont arrondies à égalité",
    "max_abs_delta_in_group": 0.0015779733657836914
  },
  {
    "line_id": "ORD-10",
    "elo": 1700,
    "cpu_top1": "b2b3",
    "gpu_top1": "d4b3",
    "cpu_top3": [
      {
        "rank": 1,
        "move_uci": "b2b3",
        "policy_probability": 0.3862626850605011
      },
      {
        "rank": 2,
        "move_uci": "d4b3",
        "policy_probability": 0.3817764222621918
      },
      {
        "rank": 3,
        "move_uci": "e2e3",
        "policy_probability": 0.0690192803740501
      }
    ],
    "gpu_top3": [
      {
        "rank": 1,
        "move_uci": "d4b3",
        "policy_probability": 0.3838083446025848
      },
      {
        "rank": 2,
        "move_uci": "b2b3",
        "policy_probability": 0.3838083446025848
      },
      {
        "rank": 3,
        "move_uci": "e2e3",
        "policy_probability": 0.0688130483031272
      }
    ],
    "qualification": "quasi-ex aequo: les deux premiers coups restent dans le top 3 et les probabilités GPU sont arrondies à égalité",
    "max_abs_delta_in_group": 0.0024543404579163153
  }
]
```

## Performance

- AMP: environ 7.55 s.
- FP32: environ 6.14 s.
- Politique complète: environ 15.46 s.
- Pic VRAM: 632516608 octets, soit environ 603.2 Mio.

## Comparaison GPU / CPU

```json
{
  "groups_left": 240,
  "groups_right": 240,
  "groups_compared": 240,
  "missing_groups": 0,
  "top1_agreement_rate": 0.9916666666666667,
  "top3_agreement_rate": 1.0,
  "mean_top10_intersection": 9.758333333333333,
  "mean_probability_correlation": 0.9999886384050891,
  "mean_absolute_difference": 0.00036436827135393873,
  "max_absolute_difference": 0.005118191242218018,
  "top1_changes": 2,
  "illegal_move_groups": 0,
  "fen_mismatches": 0
}
```

## Comparaison GPU / Lichess corrigée

Les taux ci-dessous sont calculés uniquement sur les groupes avec `lichess_total > 0`. Un groupe sans données Lichess n'est ni un accord ni un désaccord. Elo 2100 reste profilé par Maia, mais est marqué `MODEL_ONLY_NO_MATCHING_LICHESS_BAND` et exclu des dénominateurs empiriques.

```json
{
  "expected_maia_groups": 240,
  "maia_groups_observed": 240,
  "maia_groups_total": 240,
  "lichess_observed_groups": 47,
  "lichess_missing_groups": 153,
  "model_only_groups": 40,
  "detail_rows": 265,
  "overall_maia_mass_covered_by_lichess": 0.7712163925112931,
  "overall_top1_agreement_rate": 0.5319148936170213,
  "overall_top3_agreement_rate": 0.9148936170212766,
  "top1_agreement_observed_only": 0.5319148936170213,
  "top3_agreement_observed_only": 0.9148936170212766,
  "maia_mass_covered_observed_only": 0.7712163925112931,
  "true_disagreements_observed_only": 22,
  "lichess_outside_maia_top10_but_in_full_policy": 0,
  "remaining_divergences": 22,
  "by_elo": {
    "1100": {
      "groups": 40,
      "observed_groups": 5,
      "maia_mass_covered_by_lichess": 0.519894169982184,
      "top1_agreement_rate": 0.4,
      "top3_agreement_rate": 1.0,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 3
    },
    "1300": {
      "groups": 40,
      "observed_groups": 9,
      "maia_mass_covered_by_lichess": 0.5992729733032838,
      "top1_agreement_rate": 0.5555555555555556,
      "top3_agreement_rate": 0.8888888888888888,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 4
    },
    "1500": {
      "groups": 40,
      "observed_groups": 11,
      "maia_mass_covered_by_lichess": 0.7026575677914589,
      "top1_agreement_rate": 0.5454545454545454,
      "top3_agreement_rate": 0.9090909090909091,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 5
    },
    "1700": {
      "groups": 40,
      "observed_groups": 10,
      "maia_mass_covered_by_lichess": 0.7727730210418952,
      "top1_agreement_rate": 0.5,
      "top3_agreement_rate": 0.9,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 5
    },
    "1900": {
      "groups": 40,
      "observed_groups": 12,
      "maia_mass_covered_by_lichess": 0.8602706139003309,
      "top1_agreement_rate": 0.5833333333333334,
      "top3_agreement_rate": 0.9166666666666666,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 5
    },
    "2100": {
      "groups": 40,
      "observed_groups": 0,
      "maia_mass_covered_by_lichess": null,
      "top1_agreement_rate": null,
      "top3_agreement_rate": null,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 0
    }
  },
  "by_speed": {
    "blitz": {
      "groups": 44,
      "observed_groups": 44,
      "maia_mass_covered_by_lichess": 0.722961069718082,
      "top1_agreement_rate": 0.5227272727272727,
      "top3_agreement_rate": 0.8636363636363636,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 21,
      "unique_rows": 16,
      "total_positions": 236
    },
    "rapid": {
      "groups": 28,
      "observed_groups": 28,
      "maia_mass_covered_by_lichess": 0.5825338886267896,
      "top1_agreement_rate": 0.5,
      "top3_agreement_rate": 0.8928571428571429,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 14,
      "unique_rows": 12,
      "total_positions": 69
    }
  }
}
```

Synthèse observée uniquement:

- Groupes Maia totaux: 240.
- Groupes empiriquement observés Lichess: 47.
- Groupes sans données Lichess: 153.
- Groupes model-only: 40.
- Accord top 1 observé uniquement: 53.1915%.
- Accord top 3 observé uniquement: 91.4894%.
- Masse Maia couverte, observé uniquement: 0.771216.
- Vrais désaccords top 1 observés uniquement: 22.
- Réponses Lichess observées uniquement hors top 10 Maia mais dans la politique complète: 0.

Par cadence:

- Blitz: 44 groupes observés, 16 lignes uniques, 236 positions; top 1 = 52.2727%, top 3 = 86.3636%.
- Rapid: 28 groupes observés, 12 lignes uniques, 69 positions; top 1 = 50.0000%, top 3 = 89.2857%.

## Politique complète

- Masse top 10 moyenne observée dans les profils GPU: environ 0.99247, soit environ 99,25 %.
- Masse de la politique complète: environ 0.99999998, soit environ 1.
- Aucune réponse Lichess observée uniquement hors du top 10 n'a été trouvée dans la politique complète.
- La politique complète est utile pour des audits ponctuels et pour vérifier l'hypothèse top 10.
- Le top 10 reste suffisant pour le pipeline courant.

## Recommandation

`REFERENCE_MODE = CUDA_FP32`

Motifs:

- FP32 est plus rapide que l'AMP sur ce lot (6.14 s contre 7.55 s).
- La consommation VRAM observée est identique (632516608 octets).
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
