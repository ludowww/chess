# Brisez les systèmes ! — V1 Human Chess Lab

Répertoire noir francophone contre Londres, Jobava, Colle, Torre, Veresov, Stonewall et Blackmar-Diemer, destiné principalement au blitz et au rapide entre environ 1100 et 2000 Elo.

## Ce qui change par rapport à la V0.9

La V0.9 était une bibliothèque de 88 lignes accompagnée d’audits difficiles à reproduire. La V1 devient un produit éditorial vérifiable :

- **40 idées centrales** au lieu de 88 lignes présentées comme également importantes ;
- **20 lignes essentielles** pour démarrer sans surcharge ;
- **8 chapitres fondés sur les erreurs humaines**, et non seulement sur les noms d’ouvertures ;
- **48 lignes conservées en bibliothèque**, mais sorties du parcours principal ;
- un pipeline exécutable Stockfish 18 → Maia-3 → Lichess → scorecards ;
- un refus explicite de calculer un score final lorsque les preuves manquent ;
- des tests automatiques de légalité, d’unicité et de cohérence des positions.

## Statut exact

Cette livraison est une **release candidate éditoriale et technique**. Le contenu PGN est complet sur son périmètre et passe les contrôles statiques. En revanche :

- Stockfish n’a pas été réexécuté dans l’environnement de construction V1, faute de binaire local ;
- les anciens audits Stockfish sont conservés comme héritage, pas comme preuve reproduite ;
- Maia-3 79M n’a pas été exécuté, car les poids n’ont pas été téléchargés ;
- aucun export mensuel Lichess n’a été analysé dans cette livraison ;
- aucune relecture titrée ni bêta humaine n’est encore enregistrée.

Aucun taux d’erreur humaine, score pratique ou pourcentage Maia n’est donc inventé.

## Fichiers à utiliser

1. Lire `MANUSCRIT_COURS_V1.md`.
2. Étudier `PGN/00_parcours_essentiel_20.pgn`.
3. Importer ensuite les chapitres `PGN/01_...` à `PGN/08_...`.
4. Utiliser `PGN/99_cours_v1_core_40.pgn` pour un import global ou une revue.
5. Ne consulter `PGN/90_bibliotheque_v0_9_88_lignes.pgn` que comme réserve éditoriale.
6. Exécuter `LAB/run_static_qa.sh` après toute modification.

## Structure

```text
Brisez les systèmes V1/
├── MANUSCRIT_COURS_V1.md
├── CARTES_MEMOIRE_V1.md
├── PGN/
│   ├── 00_parcours_essentiel_20.pgn
│   ├── 01_... à 08_...              # 5 idées par biais humain
│   ├── 90_bibliotheque_v0_9_88_lignes.pgn
│   └── 99_cours_v1_core_40.pgn
├── DATA/
│   ├── core_40_index.csv
│   ├── scorecards_core_40_rc1.csv
│   ├── maia3_profiles_template.csv
│   ├── lichess_observations_template.csv
│   └── LEGACY_V0_9/
├── LAB/
│   ├── README_LAB.md
│   ├── config.yaml
│   ├── scripts/
│   └── tests/
├── PRODUCTION/
└── SOURCES/
```

## Commande de contrôle immédiate

```bash
cd brisez_les_systemes_v1
./LAB/run_static_qa.sh
```

Résultat attendu pour cette livraison : 40 parties, 40 identifiants uniques, aucune erreur PGN et cinq tests unitaires réussis.

## Principe directeur

> Ne pas sélectionner un coup parce qu’il est rare. Le sélectionner s’il est sain, difficile à traiter pour le palier visé, simple à jouer pour l’élève et encore valable lorsque l’adversaire connaît l’idée.
