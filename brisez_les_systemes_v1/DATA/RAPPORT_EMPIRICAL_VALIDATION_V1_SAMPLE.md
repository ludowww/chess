# Empirical validation v1 — rapport de lancement
## Statut
- Branche de travail : `work/empirical-validation-v1`.
- QA statique : OK (40 leçons, 9 tests unitaires).
- Stockfish 18 : audit 500k nodes terminé sur 436 coups noirs.
- Maia-3 : profils 5M + 79M CPU terminés, 2400 prédictions chacun.
- Lichess : extraction streamée par FIFO sur échantillons publics, sans télécharger les dumps complets. Discovery=2026-01 200k parties, validation=2026-02 200k, test=2025-12 100k.
- Scorecards : générées sur l’échantillon test Lichess ; à considérer comme **échantillon de validation**, pas vérité finale full-dump.

## Résultats clés
- Stockfish grades : {'A': 402, 'B': 19, 'C': 8, 'REVIEW': 7}
- Lichess test : 13 line_ids observés, 114 lignes de distribution.
- Scorecards : {'INSUFFICIENT_EVIDENCE': 27, 'ELIGIBLE_FOR_EDITORIAL_REVIEW': 13}

## Lignes Stockfish à revoir en priorité
- `VER-08` ply 24 `Nc5` : perte 176 cp, grade `REVIEW`, rank nan.
- `TOR-08` ply 24 `Kc7` : perte 133 cp, grade `REVIEW`, rank 5.0.
- `JOB-06` ply 16 `Qb6` : perte 131 cp, grade `REVIEW`, rank 5.0.
- `VER-05` ply 22 `Ke7` : perte 129 cp, grade `REVIEW`, rank 3.0.
- `LON-10` ply 24 `Qa5` : perte 121 cp, grade `REVIEW`, rank 3.0.
- `STO-01` ply 18 `Qa5` : perte 93 cp, grade `REVIEW`, rank 3.0.
- `TOR-09` ply 10 `f6` : perte 85 cp, grade `REVIEW`, rank 1.0.
- `JOB-10` ply 16 `Qb6` : perte 73 cp, grade `C`, rank 4.0.
- `JOB-13` ply 26 `Nxd4` : perte 66 cp, grade `C`, rank nan.
- `TOR-10` ply 20 `Nb4` : perte 66 cp, grade `C`, rank 4.0.

## Top scorecards avec données complètes sur échantillon
- `LON-02` : score 70.7, SF max loss 7, Maia proxy 100.0, Lichess error 33.3, sample max 2.0.
- `ORD-01` : score 66.7, SF max loss 40, Maia proxy 100.0, Lichess error 50.0, sample max 4.0.
- `LON-09` : score 59.8, SF max loss 14, Maia proxy 100.0, Lichess error 0.0, sample max 2.0.
- `ORD-02` : score 57.5, SF max loss 11, Maia proxy 55.5, Lichess error 13.3, sample max 9.0.
- `COL-01` : score 54.3, SF max loss 20, Maia proxy 25.2, Lichess error 0.0, sample max 5.0.
- `LON-01` : score 49.2, SF max loss 23, Maia proxy 52.5, Lichess error 0.0, sample max 3.0.
- `LON-03` : score 46.3, SF max loss 39, Maia proxy 59.6, Lichess error 0.0, sample max 2.0.
- `COL-10` : score 45.8, SF max loss 37, Maia proxy 64.8, Lichess error 0.0, sample max 2.0.

## Fichiers produits
- `DATA/static_qa_report.json` (308 bytes)
- `DATA/stockfish_v1_500k.csv` (52558 bytes)
- `DATA/maia3_5m_profiles.csv` (474284 bytes)
- `DATA/maia3_79m_profiles.csv` (478964 bytes)
- `DATA/maia3_79m_evaluated.csv` (241381 bytes)
- `DATA/lichess_discovery_2026-01_sample_200k.csv` (10798 bytes)
- `DATA/lichess_validation_2026-02_sample_200k.csv` (12042 bytes)
- `DATA/lichess_test_2025-12_sample_100k.csv` (6523 bytes)
- `DATA/lichess_test_2025-12_sample_100k_evaluated.csv` (2495 bytes)
- `DATA/maia3_vs_lichess_test_sample_comparison.csv` (31431 bytes)
- `DATA/scorecards_validated_sample.csv` (6453 bytes)
