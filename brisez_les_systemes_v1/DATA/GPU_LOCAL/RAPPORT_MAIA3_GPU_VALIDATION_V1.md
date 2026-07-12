# Rapport Maia-3 GPU validation V1

Date locale: 2026-07-13T00:43:13.7838589+02:00
Repo: C:\AI\chess
Sorties: C:\AI\chess\brisez_les_systemes_v1\DATA\GPU_LOCAL

## Environnement

``json
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
``

## Comparaison GPU / CPU

``json
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
``

## Comparaison GPU / Lichess

``json
{
  "expected_maia_groups": 240,
  "maia_groups_observed": 240,
  "detail_rows": 265,
  "overall_maia_mass_covered_by_lichess": 0.7758987853425692,
  "overall_top1_agreement_rate": 0.10416666666666667,
  "overall_top3_agreement_rate": 0.17916666666666667,
  "lichess_outside_maia_top10_but_in_full_policy": 0,
  "remaining_divergences": 215,
  "by_elo": {
    "1100": {
      "groups": 40,
      "maia_mass_covered_by_lichess": 0.5270522698050453,
      "top1_agreement_rate": 0.05,
      "top3_agreement_rate": 0.125,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 38
    },
    "1300": {
      "groups": 40,
      "maia_mass_covered_by_lichess": 0.6487973316710579,
      "top1_agreement_rate": 0.125,
      "top3_agreement_rate": 0.2,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 35
    },
    "1500": {
      "groups": 40,
      "maia_mass_covered_by_lichess": 0.704093595199725,
      "top1_agreement_rate": 0.15,
      "top3_agreement_rate": 0.25,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 34
    },
    "1700": {
      "groups": 40,
      "maia_mass_covered_by_lichess": 0.7919778856168307,
      "top1_agreement_rate": 0.125,
      "top3_agreement_rate": 0.225,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 35
    },
    "1900": {
      "groups": 40,
      "maia_mass_covered_by_lichess": 0.8652078540412692,
      "top1_agreement_rate": 0.175,
      "top3_agreement_rate": 0.275,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 33
    },
    "2100": {
      "groups": 40,
      "maia_mass_covered_by_lichess": 0.0,
      "top1_agreement_rate": 0.0,
      "top3_agreement_rate": 0.0,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 40
    }
  },
  "by_speed": {
    "blitz": {
      "groups": 44,
      "maia_mass_covered_by_lichess": 0.722961069718082,
      "top1_agreement_rate": 0.5227272727272727,
      "top3_agreement_rate": 0.8636363636363636,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 21
    },
    "rapid": {
      "groups": 28,
      "maia_mass_covered_by_lichess": 0.5825338886267896,
      "top1_agreement_rate": 0.5,
      "top3_agreement_rate": 0.8928571428571429,
      "lichess_outside_maia_top10_but_in_full_policy": 0,
      "remaining_divergences": 14
    }
  }
}
``

## Fichiers produits Ã  committer si validation acceptée

- brisez_les_systemes_v1\DATA\GPU_LOCAL\maia3_gpu_environment.json
- brisez_les_systemes_v1\DATA\GPU_LOCAL\maia3_79m_profiles_gpu_amp_run1.csv
- brisez_les_systemes_v1\DATA\GPU_LOCAL\maia3_79m_profiles_gpu_amp_run2.csv
- brisez_les_systemes_v1\DATA\GPU_LOCAL\maia3_79m_profiles_gpu_fp32.csv
- brisez_les_systemes_v1\DATA\GPU_LOCAL\maia3_79m_full_policy_gpu.csv
- brisez_les_systemes_v1\DATA\GPU_LOCAL\maia3_cpu_gpu_comparison.csv
- brisez_les_systemes_v1\DATA\GPU_LOCAL\maia3_cpu_gpu_summary.json
- brisez_les_systemes_v1\DATA\GPU_LOCAL\maia3_full_policy_gpu_vs_lichess.csv
- brisez_les_systemes_v1\DATA\GPU_LOCAL\maia3_full_policy_gpu_vs_lichess_summary.json
- brisez_les_systemes_v1\DATA\GPU_LOCAL\RAPPORT_MAIA3_GPU_VALIDATION_V1.md

## Note

Ce script ne fait aucun commit et aucun push automatiquement.
