# Empirical validation v1 — expanded Lichess run

## Statut et méthode
- Branche: `work/empirical-validation-v1`. Commit sample `efd0576` conservé comme parent; pas de réécriture.
- Extraction Lichess streamée via FIFO, sans commit de dumps `.zst`.
- Splits séparés par mois: discovery `2026-03` (1.5M parties scannées), validation `2026-04` (1M), test `2026-05` (1M).
- Bandes Elo et cadences identiques au sample: 1100-1299, 1300-1499, 1500-1699, 1700-1899, 1900-2099; blitz/rapid.
- `--max-plies 80`; ply maximal requis par le manifeste: `16`, donc couverture ouverture OK.
- Preuve finale: uniquement `DATA/lichess_test_expanded.csv`; discovery/validation servent à la stabilité/distribution, pas au scoring final.

## Tailles des échantillons expanded
| split | mois | parties scannées | lignes CSV | line_ids observés | occurrences positions-cibles uniques | max groupe |
|---|---:|---:|---:|---:|---:|---:|
| discovery | 2026-03 | 1500000 | 674 | 25 | 2199 | 121 |
| validation | 2026-04 | 1000000 | 547 | 22 | 1586 | 92 |
| test | 2026-05 | 1000000 | 542 | 23 | 1570 | 89 |

## Sample vs expanded — statuts
- Sample: `ELIGIBLE_FOR_EDITORIAL_REVIEW`=13, `INSUFFICIENT_EVIDENCE`=27.
- Expanded: `ELIGIBLE_FOR_EDITORIAL_REVIEW`=23, `INSUFFICIENT_EVIDENCE`=17.

### Lignes ayant changé de statut
| line_id | sample | expanded |
|---|---|---|
| VER-01 | INSUFFICIENT_EVIDENCE | ELIGIBLE_FOR_EDITORIAL_REVIEW |
| LON-04 | INSUFFICIENT_EVIDENCE | ELIGIBLE_FOR_EDITORIAL_REVIEW |
| TOR-10 | INSUFFICIENT_EVIDENCE | ELIGIBLE_FOR_EDITORIAL_REVIEW |
| LON-05 | INSUFFICIENT_EVIDENCE | ELIGIBLE_FOR_EDITORIAL_REVIEW |
| VER-05 | INSUFFICIENT_EVIDENCE | ELIGIBLE_FOR_EDITORIAL_REVIEW |
| LON-10 | INSUFFICIENT_EVIDENCE | ELIGIBLE_FOR_EDITORIAL_REVIEW |
| TOR-02 | INSUFFICIENT_EVIDENCE | ELIGIBLE_FOR_EDITORIAL_REVIEW |
| TOR-05 | INSUFFICIENT_EVIDENCE | ELIGIBLE_FOR_EDITORIAL_REVIEW |
| TOR-08 | INSUFFICIENT_EVIDENCE | ELIGIBLE_FOR_EDITORIAL_REVIEW |
| VER-03 | INSUFFICIENT_EVIDENCE | ELIGIBLE_FOR_EDITORIAL_REVIEW |

## Lignes encore insuffisantes
- 17 lignes restent `INSUFFICIENT_EVIDENCE`: `JOB-12`, `JOB-11`, `LON-11`, `LON-12`, `LON-15`, `PST-04`, `LON-06`, `LON-07`, `ORD-09`, `TOR-09`, `STO-01`, `ORD-10`, `JOB-06`, `JOB-09`, `JOB-10`, `VER-08`, `JOB-13`.
- Interprétation: absence ou rareté d’observation ≠ preuve que l’idée est mauvaise; la fréquence n’est pas inventée quand l’échantillon reste faible.

## Accord Maia-3 79M / Lichess expanded test
- Lignes comparées avec observation Lichess après coup clé: 17.
- Top move Lichess présent comme top-1 Maia dans au moins un Elo: 0/17.
- Top move Lichess présent dans top-3 Maia dans au moins un Elo: 1/17.
- Divergences top-3 Maia/Lichess: `BDG-01`, `COL-01`, `COL-10`, `JOB-03`, `JOB-04`, `LON-01`, `LON-02`, `LON-03`, `LON-09`, `LON-10`, `ORD-01`, `ORD-02`, `PST-01`, `TOR-05`, `VER-01`, `VER-05`.

## Résultats par cadence
- Lignes avec top réponse blitz différent du rapide: 8/11.
| line_id | blitz top | rapid top |
|---|---|---|
| BDG-01 | f1c4 | c1e3 |
| COL-01 | d3f5 | b2b3 |
| COL-10 | f1d3 | f1e2 |
| JOB-03 | c3b1 | c3b5 |
| LON-01 | b1a3 | b1d2 |
| LON-02 | c2d2 | c2c1 |
| ORD-01 | f1e2 | b1c3 |
| VER-01 | d4c5 | f1d3 |

## Résultats par Elo
- Observations par palier dans le split test (positions-cibles uniques):
  - 1100-1299: 133
  - 1300-1499: 172
  - 1500-1699: 333
  - 1700-1899: 449
  - 1900-2099: 483
- Les fréquences par Elo restent faibles pour plusieurs lignes; les conclusions doivent rester prudentes lorsque `sample` par ligne/Elo est bas.

## Stabilité discovery / validation / test
- Line_ids observés dans les trois splits: 21.
- Line_ids observés seulement partiellement ou jamais: 19 sur 40.
- Les distributions sont exploitables pour les motifs fréquents, mais beaucoup de lignes restent clairsemées; discovery/validation ne sont pas utilisés comme preuve finale.

## Lignes rares / potentiellement fortes mais non atteignables
- Lignes avec moins de 20 occurrences positions-cibles dans le test expanded: `JOB-12`, `JOB-11`, `LON-07`, `LON-06`, `LON-15`, `PST-04`, `LON-11`, `LON-12`, `JOB-10`, `VER-08`, `JOB-09`, `JOB-06`, `STO-01`, `ORD-10`, `TOR-09`, `ORD-09`, `JOB-13`, `LON-04`, `VER-03`, `TOR-05`, `LON-05`, `LON-10`, `TOR-10`, `TOR-06`, `TOR-08`, `VER-05`, `VER-01`, `LON-03`, `LON-09`.
- Ces lignes peuvent rester théoriquement fortes ou pédagogiquement utiles, mais ne sont pas assez atteignables dans ce corpus pour servir de preuve empirique finale.

## Lignes candidates à rejet ou réécriture
- Critère principal ici: alerte Stockfish / perte max élevée, pas rareté Lichess seule.
- `VER-08` — max loss Stockfish 176 cp — 4.f3 : ouvrir avant e4
- `TOR-08` — max loss Stockfish 133 cp — 4.e3 : le coup concret ...f6
- `JOB-06` — max loss Stockfish 131 cp — 4.f3 : ouvrir d4 avant l’attaque
- `VER-05` — max loss Stockfish 129 cp — 4.Bxf6 : reprendre du pion g
- `LON-10` — max loss Stockfish 121 cp — Le pion c5 “gratuit” : ...Qxb2!
- `STO-01` — max loss Stockfish 93 cp — Stonewall : fermer par ...c4!
- `TOR-09` — max loss Stockfish 85 cp — Bh4-h5-f6 : échanger puis enfermer

## Fichiers produits
- `DATA/lichess_discovery_expanded.csv` — 674 lignes, 44990 bytes.
- `DATA/lichess_validation_expanded.csv` — 547 lignes, 36652 bytes.
- `DATA/lichess_test_expanded.csv` — 542 lignes, 32957 bytes.
- `DATA/lichess_test_expanded_evaluated.csv` — 157 lignes, 14260 bytes.
- `DATA/maia3_vs_lichess_expanded_comparison.csv` — 494 lignes, 33351 bytes.
- `DATA/scorecards_validated_expanded.csv` — 40 lignes, 6973 bytes.
- `DATA/expanded_validation_summary.json` — synthèse QA reproductible.

## Limites méthodologiques
- Extraction publique Lichess limitée aux mois choisis et à 1–1.5M parties scannées par split, pas full dump.
- Les distributions Lichess sont très clairsemées sur certaines idées; aucune fréquence n’est extrapolée.
- Maia-3 est un modèle de politique humaine, pas une observation empirique; il sert de comparaison, non de preuve finale.
- Discovery, validation et test restent séparés; seul le test alimente `scorecards_validated_expanded.csv`.
