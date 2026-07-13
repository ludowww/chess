# Rapport de revue pédagogique V1.1

## Décision

Le candidat technique de 20 lignes est conservé intégralement, mais il est décliné en un parcours joueur séparé. Le PGN d’audit reste la source de traçabilité ; le nouveau PGN ne contient ni métadonnée moteur, ni commentaire de réparation, ni bilan interne.

## Ordre final

`ORD-01 → ORD-02 → COL-01 → VER-01 → COL-10 → LON-02 → LON-04 → LON-09 → LON-01 → LON-05 → LON-03 → PST-04 → LON-12 → PST-01 → TOR-02 → TOR-05 → LON-07 → JOB-09 → JOB-04 → TOR-06`

L’ordre suit les biais humains B1, B2, B3, B4, B5, B7 puis B8. À l’intérieur d’un chapitre, les lignes Essentiel précèdent les lignes Club, puis Avancé.

## Architecture joueur

- B1 — Pilotage automatique : 5 lignes
- B2 — Double cible et surcharge : 3 lignes
- B3 — Simplification trompeuse : 3 lignes
- B4 — Le gain matériel prétendument gratuit : 2 lignes
- B5 — Peur et sur-réaction : 4 lignes
- B7 — Attaque d’aile avant le centre : 1 ligne
- B8 — Géométrie tactique humanisée : 2 lignes

L’ouverture reste une métadonnée secondaire. Le parcours entraîne d’abord une erreur humaine reconnaissable, puis le coup et le plan qui y répondent.

## Longueur avant / après

| Source | Plies techniques | Plies joueur | Réduction | Titre joueur | Tier |
|---|---:|---:|---:|---|---|
| ORD-01 | 21 | 8 | 13 | Sans c3 : développer avec ...Bg4 | Essentiel |
| ORD-02 | 16 | 10 | 6 | Avec c3 : transposer vers ...Qb6 | Essentiel |
| COL-01 | 14 | 10 | 4 | Contre le Colle : sortir le fou avant ...e6 | Essentiel |
| VER-01 | 16 | 10 | 6 | Contre Nc3–Bg5 : ...c5 puis ...e6 | Essentiel |
| COL-10 | 23 | 12 | 11 | Contre le Zukertort : ...c5 puis ...Nc6 | Club |
| LON-02 | 26 | 14 | 12 | Après Qc2 : gagner un tempo avec ...Bf5 | Essentiel |
| LON-04 | 25 | 14 | 11 | Après Qc1 : ouvrir la colonne c avec ...cxd4 | Club |
| LON-09 | 22 | 14 | 8 | Après b3 : déplacer la cible vers f3 avec ...Bg4 | Club |
| LON-01 | 26 | 16 | 10 | Après Qxb6 : reprendre avec ...axb6 | Essentiel |
| LON-05 | 26 | 16 | 10 | Après cxd4 : développer avec ...Bf5 | Club |
| LON-03 | 31 | 16 | 15 | Dans la finale : fixer l’aile-dame avec ...b5 | Avancé |
| PST-04 | 12 | 8 | 4 | Après Bxh6? : accepter avec ...Rxh6 | Essentiel |
| LON-12 | 26 | 14 | 12 | Bd3 oublie b2 : ...Qxb2 puis ...Qxc3 | Avancé |
| PST-01 | 17 | 8 | 9 | Contre 2.Bg5 : demander au fou avec ...h6 | Essentiel |
| TOR-02 | 23 | 8 | 15 | Après Bh4 : restreindre le fou avec ...h5 | Club |
| TOR-05 | 17 | 12 | 5 | Contre h4 : répondre au centre avec ...c5 | Club |
| LON-07 | 25 | 20 | 5 | Chasser le fou : ...h6 puis ...g5 | Club |
| JOB-09 | 27 | 10 | 17 | Après Qxd4 : gagner un tempo avec ...Nc6 | Club |
| JOB-04 | 22 | 8 | 14 | Après Nb5 : exploiter le roi avec ...Qa5+ | Essentiel |
| TOR-06 | 25 | 10 | 15 | Nbd2 : échanger avec ...Nxg5, puis jouer ...e5 | Club |

Le parcours passe de 440 plies techniques cumulés à 238 plies joueur. Les continuations supprimées restent disponibles dans `99_cours_v1_1_candidate.pgn`.

## Titres et coups enseignés

Chaque titre nomme désormais la décision réellement entraînée. Les corrections principales sont :

- `COL-01` enseigne `...Bf5`, et non le coup suivant `...e6`.
- `VER-01` enseigne la rupture `...c5`.
- `LON-01` enseigne la reprise `...axb6`.
- `LON-04` enseigne `...cxd4` avant le développement du fou.
- `LON-12` enseigne `...Qxb2` uniquement avec la sortie `...Qxc3`.
- `TOR-06` enseigne l’échange `...Nxg5`, suivi de `...e5`.

## Calibration des tiers

### Essentiel

`ORD-01`, `ORD-02`, `COL-01`, `VER-01`, `LON-02`, `LON-01`, `PST-04`, `PST-01`, `JOB-04`

### Club

`COL-10`, `LON-04`, `LON-09`, `LON-05`, `JOB-09`, `TOR-02`, `LON-07`, `TOR-05`, `TOR-06`

### Avancé

`LON-03`, `LON-12`

## Nettoyage éditorial

Le parcours joueur retire toutes les traces de fabrication : réparation, gate, centipions, moteur, FEN et bilan d’audit. Chaque ligne porte un commentaire unique structuré en quatre éléments courts : idée, raison, suite et mémo.

La formulation de `PST-04` est corrigée : un seul pion a été capturé avant `...Rxh6`. Le mémo joueur est désormais : « Un pion ne vaut pas un fou ; la tour h6 peut revenir. »

## B6 gap review

Le noyau ne contient actuellement aucune ligne B6. Trois options ont été comparées sans modifier le core :

1. **BDG-01** — meilleur candidat de couverture. Il ajoute un vrai système secondaire, possède l’échantillon Lichess exact le plus fourni des trois options et correspond bien à une règle rigide de gambit. Il nécessite toutefois une nouvelle coupe ou une réévaluation ciblée, car la ligne technique historique dépassait légèrement le seuil PASS.
2. **ORD-09** — moteur naturellement sain, mais absence d’échantillon exact et redondance London importante.
3. **Remplacer une ligne London** — `LON-09` est la candidate la plus facile à sacrifier si B6 entre, car son idée `...Bg4` recoupe partiellement `ORD-01`. `LON-05` doit être conservée de préférence : elle couvre la reprise `cxd4` et le plan sur b4, absent ailleurs.

### Recommandation B6

Tester `BDG-01` dans une passe séparée, face à `LON-09`. Ne pas modifier les 20 lignes tant que le préfixe joueur de `BDG-01` n’a pas reçu le même audit que le candidat V1.1.

## Validation attendue

- 20 parties et mêmes `SourceLineID` que le candidat technique.
- Chaque partie joueur est un préfixe exact de sa partie technique.
- Toutes les lignes se terminent après un coup noir.
- Le commentaire principal est placé sur le coup enseigné et reste sous 90 mots.
- Aucun texte interne de laboratoire n’apparaît dans le parcours.
