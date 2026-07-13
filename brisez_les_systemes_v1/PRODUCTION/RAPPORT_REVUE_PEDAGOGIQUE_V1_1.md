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

## Commentaires pédagogiques

Le parcours contient désormais **73 interventions pédagogiques** réparties dans les 20 leçons :

- 20 **Repères** présentent la structure et l’idée adverse avant la séquence ;
- 20 **Déclencheurs** expliquent pourquoi le dernier coup blanc autorise la réponse noire ;
- 20 commentaires **Le coup** donnent la fonction exacte du coup entraîné ;
- 13 commentaires **Plan** accompagnent les lignes qui montrent une décision noire supplémentaire.

Chaque leçon contient trois ou quatre commentaires positionnels, pour un total de 96 à 139 mots. Aucun commentaire isolé ne dépasse 75 mots. Le texte est distribué au moment où l’information devient utile : reconnaître la position, choisir le coup, comprendre sa fonction, puis savoir quoi faire ensuite.

Chaque leçon inclut également :

- une règle **À retenir** ;
- une **Erreur à éviter** propre à la position ;
- un plan conditionnel plutôt qu’une simple liste de coups ;
- une explication de ce que le coup ne cherche pas à accomplir lorsque le risque de mauvaise interprétation est important.

Les formulations génériques et les traces de fabrication ont été retirées. Les commentaires ne parlent ni de réparation, ni de gate, ni de moteur, ni de centipions. La formulation de `PST-04` est corrigée : un seul pion a été capturé avant `...Rxh6`, et le mémo est « Un pion ne vaut pas un fou ; la tour h6 peut revenir. »

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
- Trois ou quatre commentaires pédagogiques par leçon.
- Le commentaire précédent le coup entraîné commence par `Déclencheur :`.
- Le commentaire du coup entraîné commence par `Le coup :`.
- Chaque leçon contient `À retenir :` et `Erreur à éviter :`.
- Entre 80 et 160 mots pédagogiques par leçon.
- Aucun commentaire isolé au-dessus de 75 mots.
- Aucun texte interne de laboratoire dans le parcours.
