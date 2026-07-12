# Empirical validation v1 — corrected Maia/scorecard gates

## Correction méthodologique
- Les anciens profils Maia et les anciens statuts de promotion sont invalidés par le bug de positionnement Maia: le profilage utilisait une FEN quatre champs sans historique réel.
- Le run corrigé reconstruit chaque position depuis `fixed_prefix` et appelle Maia via `position startpos moves <historique UCI complet>`.
- Contrôle anti-position initiale: `0` ligne Maia corrigée sur la position initiale; mismatches FEN: `0`.
- CUDA indisponible sur cette machine; `maia3-79m` a été exécuté sur CPU avec le meilleur matériel local disponible.

## Accord Maia-3 corrigé / Lichess expanded test
- Lignes comparées: 17.
- Accord top 1: 8/17.
- Accord top 3: 12/17.
- Masse moyenne de probabilité Maia couverte par les réponses Lichess: 0.663.
- Divergences restantes top-3: COL-01, COL-10, TOR-02, TOR-05, VER-01.

### Accord par Elo
| Elo | lignes | top1 | top3 | masse Maia couverte |
|---:|---:|---:|---:|---:|
| 1100 | 17 | 8 | 13 | 0.616 |
| 1300 | 17 | 9 | 13 | 0.652 |
| 1500 | 17 | 9 | 14 | 0.672 |
| 1700 | 17 | 9 | 13 | 0.685 |
| 1900 | 17 | 9 | 13 | 0.686 |
| 2100 | 17 | 7 | 14 | 0.669 |

### Accord blitz/rapide
| cadence | lignes | top1 | top3 | masse Maia couverte |
|---|---:|---:|---:|---:|
| blitz | 16 | 9 | 14 | 0.670 |
| rapid | 12 | 8 | 10 | 0.658 |

## Scorecards corrigées
- Anciens statuts de complétude: `{'ELIGIBLE_FOR_EDITORIAL_REVIEW': 23, 'INSUFFICIENT_EVIDENCE': 17}`.
- Nouveaux `evidence_status`: `{'MODEL_AND_ENGINE_ONLY': 37, 'LIMITED_TEST_DATA': 3}`.
- Nouveaux `engine_gate`: `{'PASS': 16, 'REJECT': 14, 'REVIEW': 10}`.
- Nouveaux `empirical_sample_gate`: `{'INSUFFICIENT': 37, 'LIMITED': 3}`.
- Recommandations éditoriales: `{'ENGINE_REJECT': 14, 'ENGINE_REVIEW': 10, 'LIMITED_EMPIRICAL_SUPPORT': 9, 'INSUFFICIENT_EVIDENCE': 7}`.
- Réellement `EDITORIAL_REVIEW_READY`: 0 lignes — aucune.
- `ENGINE_REJECT`: 14 — JOB-12, TOR-10, VER-05, LON-10, LON-15, TOR-08, TOR-09, STO-01, JOB-06, JOB-10, VER-08, JOB-03, JOB-13, VER-03.
- `ENGINE_REVIEW`: 10 — ORD-01, COL-10, LON-04, LON-03, LON-07, TOR-05, BDG-01, ORD-10, JOB-09, TOR-06.
- Limitées par rareté / preuves insuffisantes: 16 — ORD-02, COL-01, VER-01, LON-02, LON-09, LON-01, LON-05, JOB-11, LON-11, LON-12, PST-04, LON-06, TOR-02, PST-01, ORD-09, JOB-04.

## Impact de la correction Maia
- La correction supprime la contamination par position initiale et rend les coups Maia légaux dans les positions cibles.
- L’accord top 1 devient non nul après correction, mais les divergences restantes doivent être examinées ligne par ligne.

## Fichiers produits
- `DATA/maia3_5m_profiles_corrected.csv` — 465709 bytes.
- `DATA/maia3_79m_profiles_corrected.csv` — 468033 bytes.
- `DATA/maia3_79m_evaluated_corrected.csv` — 607953 bytes.
- `DATA/maia3_vs_lichess_expanded_comparison_corrected.csv` — 31443 bytes.
- `DATA/scorecards_validated_expanded_corrected.csv` — 10954 bytes.
- `DATA/corrected_validation_summary.json` — 2994 bytes.
