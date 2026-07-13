# Rapport refonte éditoriale V1.1
## Synthèse
- Taille V1 : 40 lignes.
- Taille proposée V1.1 : 22 lignes.
- KEEP_CORE : 26
- REPAIR_CONTINUATION : 0
- REPLACE_KEY_MOVE : 0
- SIDELINE_ONLY : 14
- DROP : 0

Preuve GPU utilisée uniquement comme confirmation méthodologique : CPU/GPU top 3 identique, top 1 Maia/Lichess observé environ 53 %, top 3 environ 91,5 %, top 10 environ 99,25 %. Ces chiffres ne sont pas interprétés comme fréquence réelle de jeu.

## Distribution coup-clé
- PASS : 40
- REVIEW : 0
- REJECT : 0

## Audit des 16 lignes précédemment PASS
- ORD-02 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- COL-01 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- VER-01 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- LON-02 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- LON-09 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- LON-01 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- LON-05 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- JOB-11 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- LON-11 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- LON-12 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- PST-04 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- LON-06 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- TOR-02 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- PST-01 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- ORD-09 : KEEP_CORE — reste dans le core. Coup-clé sain et pas de défaut moteur critique dans la ligne principale.
- JOB-04 : KEEP_CORE — devient sideline (rareté/redondance). Coup-clé sain et pas de défaut moteur critique dans la ligne principale.

## Audit des 10 lignes REVIEW
- ORD-01 : coup-clé sain (PASS, 0 cp) ; première imprécision LATER_CONTINUATION_REVIEW ; réparation proposée: f6 (SIDELINE_ONLY) ; décision KEEP_CORE.
- COL-10 : coup-clé sain (PASS, 0 cp) ; première imprécision LATER_CONTINUATION_REVIEW ; réparation proposée: Qc7 (SIDELINE_ONLY) ; décision KEEP_CORE.
- LON-04 : coup-clé sain (PASS, 1 cp) ; première imprécision LATER_CONTINUATION_REVIEW ; réparation proposée: Rc8 (SIDELINE_ONLY) ; décision KEEP_CORE.
- LON-03 : coup-clé sain (PASS, 0 cp) ; première imprécision LATER_CONTINUATION_REVIEW ; réparation proposée: Bf5 (SIDELINE_ONLY) ; décision KEEP_CORE.
- LON-07 : coup-clé sain (PASS, 18 cp) ; première imprécision LATER_CONTINUATION_REVIEW ; réparation proposée: Bf5 (SIDELINE_ONLY) ; décision KEEP_CORE.
- TOR-05 : coup-clé sain (PASS, 0 cp) ; première imprécision LATER_CONTINUATION_REVIEW ; réparation proposée: Qb6 (SIDELINE_ONLY) ; décision KEEP_CORE.
- BDG-01 : coup-clé sain (PASS, 17 cp) ; première imprécision NO_ENGINE_FAILURE ; aucune réparation simple retenue ; décision KEEP_CORE.
- ORD-10 : coup-clé sain (PASS, 0 cp) ; première imprécision LATER_CONTINUATION_REVIEW ; réparation proposée: a6 (SIDELINE_ONLY) ; décision KEEP_CORE.
- JOB-09 : coup-clé sain (PASS, 0 cp) ; première imprécision LATER_CONTINUATION_REVIEW ; réparation proposée: d4 (SIDELINE_ONLY) ; décision KEEP_CORE.
- TOR-06 : coup-clé sain (PASS, 0 cp) ; première imprécision LATER_CONTINUATION_REVIEW ; réparation proposée: Bd6 (SIDELINE_ONLY) ; décision KEEP_CORE.

## Audit des 14 lignes REJECT
- JOB-12 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- TOR-10 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- VER-05 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- LON-10 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- LON-15 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- TOR-08 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- TOR-09 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- STO-01 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- JOB-06 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- JOB-10 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- VER-08 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- JOB-03 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- JOB-13 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.
- VER-03 : coup-clé sain mais continuation ultérieure mauvaise ; premier défaut LATER_CONTINUATION_REJECT ; concept récupérable en sideline/réparation ; décision SIDELINE_ONLY.

## Noyau V1.1 proposé
1. V11-01-ORD-01 ← ORD-01 — 2.Bf4 : ...c5 puis le clouage ...Bg4 (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
2. V11-02-ORD-02 ← ORD-02 — 2.Bf4 et 3.c3 : revenir au plan ...Nc6 (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
3. V11-03-COL-01 ← COL-01 — 3.e3 : sortir le fou avec ...Bf5 (KEEP_CORE, COLLE_LIGHT_SQUARE_DEVELOPMENT)
4. V11-04-COL-10 ← COL-10 — Zukertort : frapper par ...c5 (KEEP_CORE, COLLE_LIGHT_SQUARE_DEVELOPMENT)
5. V11-05-VER-01 ← VER-01 — 3...c5 : attaquer d4 immédiatement (KEEP_CORE, VERESOV_CENTER_BREAK)
6. V11-06-LON-02 ← LON-02 — La dame recule en c2 : ...Bf5 (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
7. V11-07-LON-04 ← LON-04 — Qc1 et reprise par le pion e (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
8. V11-08-LON-09 ← LON-09 — b3 protège b2 : développer avec ...Bg4 (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
9. V11-09-LON-01 ← LON-01 — La dame blanche s’échange : ...c4! (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
10. V11-10-LON-03 ← LON-03 — La finale asymétrique : le plan ...b5 (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
11. V11-11-LON-05 ← LON-05 — Qc1 et reprise par le pion c (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
12. V11-12-JOB-11 ← JOB-11 — 4.Bxb8 : reprendre avec la tour (KEEP_CORE, JOBAVA_CENTER_BREAK)
13. V11-13-LON-11 ← LON-11 — Nbd2 laisse b2 : la route de sortie ...Qxc3 (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
14. V11-14-LON-12 ← LON-12 — Bd3 oublie b2 (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
15. V11-15-PST-04 ← PST-04 — 3.Bxh6? : accepter le sacrifice (KEEP_CORE, SECONDARY_SYSTEM_CENTER_RESPONSE)
16. V11-16-LON-06 ← LON-06 — Qc2 : poser la question avec ...Nh5 (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
17. V11-17-LON-07 ← LON-07 — Le fou se cache en g5 : ...h6 et ...g5 (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
18. V11-18-TOR-02 ← TOR-02 — 4.Bh4 : le coup machine ...h5! (KEEP_CORE, TORRE_E4_BISHOP_PRESSURE)
19. V11-19-TOR-05 ← TOR-05 — 4.h4 : ignorer l’intimidation (KEEP_CORE, TORRE_E4_BISHOP_PRESSURE)
20. V11-20-PST-01 ← PST-01 — 2.Bg5 : demander au fou avec ...h6 (KEEP_CORE, SECONDARY_SYSTEM_CENTER_RESPONSE)
21. V11-21-ORD-09 ← ORD-09 — h4 précoce : riposter au centre (KEEP_CORE, LONDON_QB6_DOUBLE_PRESSURE)
22. V11-22-BDG-01 ← BDG-01 — Blackmar-Diemer : accepter avec ...exf3 (KEEP_CORE, VERESOV_CENTER_BREAK)

## Sidelines
- JOB-12 — Jobava : rupture centrale et cases noires : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- TOR-10 — Torre : pression sur e4 et question au fou : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- VER-05 — Veresov : rupture centrale et développement sobre : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- LON-10 — Londres : ...Qb6, d4 et b2 sous pression : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- LON-15 — Londres : ...Qb6, d4 et b2 sous pression : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- TOR-08 — Torre : pression sur e4 et question au fou : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- TOR-09 — Torre : pression sur e4 et question au fou : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- STO-01 — Systèmes secondaires : répondre au centre : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- JOB-06 — Jobava : rupture centrale et cases noires : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- JOB-10 — Jobava : rupture centrale et cases noires : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- VER-08 — Veresov : rupture centrale et développement sobre : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- JOB-03 — Jobava : rupture centrale et cases noires : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- JOB-13 — Jobava : rupture centrale et cases noires : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.
- VER-03 — Veresov : rupture centrale et développement sobre : Le concept du coup-clé tient, mais la suite doit être réparée avant MoveTrainer central.

## Familles
- COLLE_LIGHT_SQUARE_DEVELOPMENT — Colle/Zukertort : développement et cases centrales : 2 lignes, structure/objectif noir comparables ; réponse humaine et règle mémoire réutilisables.
- JOBAVA_CENTER_BREAK — Jobava : rupture centrale et cases noires : 8 lignes, structure/objectif noir comparables ; réponse humaine et règle mémoire réutilisables.
- LONDON_QB6_DOUBLE_PRESSURE — Londres : ordres de coups et double pression : 16 lignes, structure/objectif noir comparables ; réponse humaine et règle mémoire réutilisables.
- SECONDARY_SYSTEM_CENTER_RESPONSE — Systèmes secondaires : répondre au centre : 3 lignes, structure/objectif noir comparables ; réponse humaine et règle mémoire réutilisables.
- TORRE_E4_BISHOP_PRESSURE — Torre : pression sur e4 et question au fou : 6 lignes, structure/objectif noir comparables ; réponse humaine et règle mémoire réutilisables.
- VERESOV_CENTER_BREAK — Veresov : rupture centrale et développement sobre : 5 lignes, structure/objectif noir comparables ; réponse humaine et règle mémoire réutilisables.

## Questions humaines restantes
- La rareté exacte d'une position doit-elle sortir une ligne du MoveTrainer central malgré sa santé moteur ?
- La réparation proposée est-elle mémorisable pour un joueur 1000–1800 ou seulement techniquement bonne ?
- Certaines familles se recouvrent-elles trop dans l'expérience Chessable réelle ?
- Le ton des commentaires conserve-t-il décision + plan + règle mémoire sans promesse commerciale excessive ?
