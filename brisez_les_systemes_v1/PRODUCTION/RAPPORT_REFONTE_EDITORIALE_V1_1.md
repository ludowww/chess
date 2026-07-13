# Rapport refonte éditoriale V1.1
## Synthèse
- Taille V1 : 40 lignes.
- Taille noyau candidat V1.1 : 20 lignes.
- KEEP_CORE : 14
- REPAIR_CONTINUATION : 9
- REPLACE_KEY_MOVE : 0
- SIDELINE_ONLY : 17
- DROP : 0
- Règle appliquée : KEEP_CORE seulement si coup-clé PASS, aucun défaut de continuation, et perte maximale <=25 cp.
- Les continuations REVIEW/REJECT retenues dans le noyau passent par REPAIR_CONTINUATION avec remplacement <=25 cp, concept conservé, complexité SIMPLE/MODERATE.

## Composition finale du core
1. V11-01-ORD-01 ← ORD-01 — 2.Bf4 : ...c5 puis le clouage ...Bg4 (REPAIR_CONTINUATION, LONDON_EARLY_C5_BG4) — réparation f6 au FEN exact
2. V11-02-ORD-02 ← ORD-02 — 2.Bf4 et 3.c3 : revenir au plan ...Nc6 (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
3. V11-03-COL-01 ← COL-01 — 3.e3 : sortir le fou avec ...Bf5 (KEEP_CORE, COLLE_BF5_DEVELOPMENT)
4. V11-04-COL-10 ← COL-10 — Zukertort : frapper par ...c5 (REPAIR_CONTINUATION, COLLE_ZUKERTORT_C5_QC7) — réparation Qc7 au FEN exact
5. V11-05-VER-01 ← VER-01 — 3...c5 : attaquer d4 immédiatement (KEEP_CORE, VERESOV_CENTER_BREAK)
6. V11-06-LON-02 ← LON-02 — La dame recule en c2 : ...Bf5 (KEEP_CORE, LONDON_QC1_CXD4_STRUCTURE)
7. V11-07-LON-04 ← LON-04 — Qc1 et reprise par le pion e (REPAIR_CONTINUATION, LONDON_QC1_CXD4_STRUCTURE) — réparation Rc8 au FEN exact
8. V11-08-LON-09 ← LON-09 — b3 protège b2 : développer avec ...Bg4 (KEEP_CORE, LONDON_EARLY_C5_BG4)
9. V11-09-LON-01 ← LON-01 — La dame blanche s’échange : ...c4! (KEEP_CORE, LONDON_QB3_C4_ENDGAME)
10. V11-10-LON-03 ← LON-03 — La finale asymétrique : le plan ...b5 (REPAIR_CONTINUATION, LONDON_QB3_C4_ENDGAME) — réparation Bf5 au FEN exact
11. V11-11-LON-05 ← LON-05 — Qc1 et reprise par le pion c (KEEP_CORE, LONDON_QC1_CXD4_STRUCTURE)
12. V11-12-JOB-09 ← JOB-09 — 4.a3 : un tempo décoratif (REPAIR_CONTINUATION, JOBAVA_TEMPO_CENTER_BREAK) — réparation d4 au FEN exact
13. V11-13-PST-04 ← PST-04 — 3.Bxh6? : accepter le sacrifice (KEEP_CORE, PSEUDO_TROMP_BISHOP_SAC)
14. V11-14-LON-12 ← LON-12 — Bd3 oublie b2 (KEEP_CORE, LONDON_QB2_QUEEN_RAID)
15. V11-15-TOR-02 ← TOR-02 — 4.Bh4 : le coup machine ...h5! (KEEP_CORE, TORRE_H4_H5_BISHOP_TRAP)
16. V11-16-PST-01 ← PST-01 — 2.Bg5 : demander au fou avec ...h6 (KEEP_CORE, PSEUDO_TROMP_H6_CENTER)
17. V11-17-LON-07 ← LON-07 — Le fou se cache en g5 : ...h6 et ...g5 (REPAIR_CONTINUATION, LONDON_NH5_BISHOP_HUNT) — réparation Bf5 au FEN exact
18. V11-18-TOR-06 ← TOR-06 — 4.Nbd2 : prendre le fou (REPAIR_CONTINUATION, TORRE_NBD2_EXCHANGE_CENTER) — réparation Bd6 au FEN exact
19. V11-19-TOR-05 ← TOR-05 — 4.h4 : ignorer l’intimidation (REPAIR_CONTINUATION, TORRE_H4_CENTER_RESPONSE) — réparation Qb6 au FEN exact
20. V11-20-JOB-04 ← JOB-04 — 4.Nb5 : l’échec qui casse le schéma (KEEP_CORE, JOBAVA_NB5_CHECK_RESPONSE)

## Variantes naturellement PASS
- COL-01 — Colle/Zukertort : sortir le fou avant e6 ; max V1 avant candidat 20 cp.
- JOB-04 — Jobava : Nb5+, développement et roi sûr ; max V1 avant candidat 19 cp.
- LON-01 — Londres : Qb3, ...c4 et finale axb6 ; max V1 avant candidat 23 cp.
- LON-02 — Londres : dame blanche passive, centre clarifié ; max V1 avant candidat 7 cp.
- LON-05 — Londres : dame blanche passive, centre clarifié ; max V1 avant candidat 17 cp.
- LON-09 — Londres : développement sobre quand b2 est protégé ; max V1 avant candidat 14 cp.
- LON-12 — Londres : raid de dame sur b2/c3 ; max V1 avant candidat 14 cp.
- ORD-02 — Londres : ...Qb6, d4 et b2 sous pression ; max V1 avant candidat 11 cp.
- PST-01 — Pseudo-Trompowsky : demander au fou puis centre ; max V1 avant candidat 21 cp.
- PST-04 — Pseudo-Trompowsky : sacrifice de fou insuffisant ; max V1 avant candidat 17 cp.
- TOR-02 — Torre : ...h5 et restriction du fou ; max V1 avant candidat 16 cp.
- VER-01 — Veresov : rupture centrale et développement sobre ; max V1 avant candidat 9 cp.

## Variantes réparées
- COL-10 : Nd7 → Qc7 (d8c7), FEN r1bq1rk1/pp3ppp/2nbpn2/3pN3/3P4/1P1B4/PBP2PPP/RN1Q1RK1 b - - 4 9, perte réparation 0 cp, suite Qc7 Re1 Nb4 Ba3 Rd8 c3.
- JOB-09 : Qa5+ → d4 (d5d4), FEN r2qkb1r/pp1b1p1p/4np2/1N1pp3/7Q/P3P3/1PP2PPP/R3KBNR b KQkq - 1 11, perte réparation 0 cp, suite d4 O-O-O a6 Nxd4 exd4 Nf3.
- LON-03 : Bh6 → Bf5 (c8f5), FEN r1b1kb1r/1p2pp2/2n2n2/1p1pN2p/2pP2pP/2P1P1B1/PP1NBPP1/R4RK1 b kq - 1 13, perte réparation 0 cp, suite Bf5 a4 bxa4 Nxc6 bxc6 Ra2.
- LON-04 : Rg8 → Rc8 (a8c8), FEN r3kb1r/pp2pp2/1qn2n1p/3p1bp1/3P4/2P2N1P/PP2BPPB/RNQ1K2R b KQkq - 1 10, perte réparation 0 cp, suite Rc8 Nbd2 h5 Nb3 g4 Nh4.
- LON-07 : Nb4 → Bf5 (c8f5), FEN r1b1kb1r/pp2pp2/1qn4p/3p2pn/3P4/4PNB1/PPQ2PPP/RN2KB1R b KQkq - 0 10, perte réparation 0 cp, suite Bf5 Qe2 a6 a3 g4 Nh4.
- ORD-01 : Nge7 → f6 (f7f6), FEN r3kbnr/pp1q1ppp/2n1p3/3p4/3P1Bb1/1QP2N2/PP1N1PPP/R3KB1R b KQkq - 3 8, perte réparation 0 cp, suite f6 Be2 g5 Bg3 Bf5 O-O.
- TOR-05 : f6 → Qb6 (d8b6), FEN r1bqkb1r/pp2pppp/2n5/2pp2B1/3Pn2P/4PN2/PPPN1PP1/R2QKB1R b KQkq - 2 6, perte réparation 0 cp, suite Qb6 Nxe4 dxe4 Nd2 cxd4 exd4.
- TOR-06 : Qb6 → Bd6 (f8d6), FEN r1bqkb1r/pp3ppp/2n5/3p4/3Pp3/4P3/PP1N1PPP/R2QKBNR b KQkq - 0 10, perte réparation 0 cp, suite Bd6 Ne2 Bg4 a3 O-O Rc1.

## Concepts sains sortis pour rareté / redondance / difficulté humaine

### Sorties pour rareté
- JOB-12 — Jobava : retrait Nb1 et double pression : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- TOR-10 — Torre : ...Qb6, e4 et b2 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- JOB-11 — Jobava : Bxb8 et activité de tour : Concept sain mais échantillon empirique trop rare pour priorité core. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- VER-05 — Veresov : structure gxf6 et centre : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess OBSERVED, n=1).
- LON-10 — Londres : raid de dame sur b2/c3 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess OBSERVED, n=1).
- LON-11 — Londres : raid de dame sur b2/c3 : Concept sain mais échantillon empirique trop rare pour priorité core. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- LON-15 — Londres : raid de dame sur b2/c3 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- LON-06 — Londres : ...Nh5 et chasse du fou : Concept sain et variante naturellement PASS sur l'audit V1. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- ORD-09 — Aile précoce : répondre au centre : Concept sain et variante naturellement PASS sur l'audit V1. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- TOR-08 — Torre : e3, ...f6-g5 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- TOR-09 — Torre : route Bh4-h5-f6 et échange : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- STO-01 — Stonewall : fixer par ...c4 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- ORD-10 — Londres : tempos h3/h4 et chasse du fou : Continuation REVIEW réparée par une alternative <=25 cp, concept conservé, complexité simple/modérée. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- JOB-06 — Jobava : f3, ouvrir avant e4 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- JOB-10 — Jobava : tempos d’aile, centre d’abord : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- VER-08 — Veresov : f3, ouvrir avant e4 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- JOB-03 — Jobava : dxc5, rupture centrale : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess OBSERVED, n=4).
- JOB-13 — Jobava : clouage puis motif ...Qa5+ : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- VER-03 — Veresov : dxc5, rendre par le centre : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).

### Sorties pour redondance
- LON-10 — Londres : raid de dame sur b2/c3 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess OBSERVED, n=1).
- LON-15 — Londres : raid de dame sur b2/c3 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- LON-06 — Londres : ...Nh5 et chasse du fou : Concept sain et variante naturellement PASS sur l'audit V1. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- ORD-09 — Aile précoce : répondre au centre : Concept sain et variante naturellement PASS sur l'audit V1. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- ORD-10 — Londres : tempos h3/h4 et chasse du fou : Continuation REVIEW réparée par une alternative <=25 cp, concept conservé, complexité simple/modérée. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).

### Sorties pour difficulté humaine ou continuation non réparée
- JOB-12 — Jobava : retrait Nb1 et double pression : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- TOR-10 — Torre : ...Qb6, e4 et b2 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- JOB-11 — Jobava : Bxb8 et activité de tour : Concept sain mais échantillon empirique trop rare pour priorité core. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- VER-05 — Veresov : structure gxf6 et centre : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess OBSERVED, n=1).
- LON-10 — Londres : raid de dame sur b2/c3 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess OBSERVED, n=1).
- LON-11 — Londres : raid de dame sur b2/c3 : Concept sain mais échantillon empirique trop rare pour priorité core. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- LON-15 — Londres : raid de dame sur b2/c3 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- TOR-08 — Torre : e3, ...f6-g5 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- TOR-09 — Torre : route Bh4-h5-f6 et échange : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- STO-01 — Stonewall : fixer par ...c4 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- BDG-01 — Blackmar-Diemer : accepter puis développer : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess OBSERVED, n=36).
- JOB-06 — Jobava : f3, ouvrir avant e4 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- JOB-10 — Jobava : tempos d’aile, centre d’abord : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- VER-08 — Veresov : f3, ouvrir avant e4 : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- JOB-03 — Jobava : dxc5, rupture centrale : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess OBSERVED, n=4).
- JOB-13 — Jobava : clouage puis motif ...Qa5+ : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).
- VER-03 — Veresov : dxc5, rendre par le centre : Continuation REJECT ou réparation insuffisante : hors noyau. (Maia AVAILABLE, Lichess NO_EXACT_POSITION_SAMPLE, n=0).

## Distribution par famille
- LONDON_EARLY_C5_BG4 — Londres : ...c5 puis ...Bg4 sans sortie de dame : 2
- LONDON_QB6_DOUBLE_PRESSURE — Londres : ...Qb6, d4 et b2 sous pression : 1
- COLLE_BF5_DEVELOPMENT — Colle/Zukertort : sortir le fou avant e6 : 1
- COLLE_ZUKERTORT_C5_QC7 — Colle/Zukertort : ...c5 puis coordination ...Qc7 : 1
- VERESOV_CENTER_BREAK — Veresov : rupture centrale et développement sobre : 1
- LONDON_QC1_CXD4_STRUCTURE — Londres : dame blanche passive, centre clarifié : 3
- LONDON_QB3_C4_ENDGAME — Londres : Qb3, ...c4 et finale axb6 : 2
- JOBAVA_TEMPO_CENTER_BREAK — Jobava : tempos d’aile, centre d’abord : 1
- PSEUDO_TROMP_BISHOP_SAC — Pseudo-Trompowsky : sacrifice de fou insuffisant : 1
- LONDON_QB2_QUEEN_RAID — Londres : raid de dame sur b2/c3 : 1
- TORRE_H4_H5_BISHOP_TRAP — Torre : ...h5 et restriction du fou : 1
- PSEUDO_TROMP_H6_CENTER — Pseudo-Trompowsky : demander au fou puis centre : 1
- LONDON_NH5_BISHOP_HUNT — Londres : ...Nh5/...h6/...g5 et chasse du fou : 1
- TORRE_NBD2_EXCHANGE_CENTER — Torre : Nbd2, échange puis centre : 1
- TORRE_H4_CENTER_RESPONSE — Torre : h4, répondre par le centre : 1
- JOBAVA_NB5_CHECK_RESPONSE — Jobava : Nb5+, développement et roi sûr : 1

## Distribution par système
- LONDON : 10
- COLLE_ZUKERTORT : 2
- VERESOV_PSEUDO_TROMP : 3
- JOBAVA : 2
- TORRE : 3

## Preuves Maia/Lichess utilisées
- Source scorecards : DATA/scorecards_validated_expanded_corrected.csv.
- Source synthèse corrigée : DATA/corrected_validation_summary.json.
- Source GPU full-policy : DATA/GPU_LOCAL/maia3_full_policy_gpu_vs_lichess_summary.json.
- Groupes Maia GPU observés : 240 ; top3 agreement full-policy/Lichess : 0.17916666666666667.
- La rareté ne condamne pas automatiquement un concept sain ; elle baisse la priorité core, le poids MoveTrainer et signale un besoin de bêta humaine.

## Note audit moteur candidat
Le PGN candidat doit être réaudité dans DATA/stockfish_v1_1_candidate_500k.csv, puis les commentaires BILAN V1.1 sont régénérés exclusivement depuis ce CSV.
