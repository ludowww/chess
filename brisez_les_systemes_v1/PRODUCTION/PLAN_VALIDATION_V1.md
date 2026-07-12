# Plan de validation V1

## Porte 1 — Légalité et cohérence

- 40 identifiants uniques ;
- toutes les séquences légales ;
- FEN avant/après cohérentes avec le coup-clé ;
- aucun chapitre contenant une partie non référencée.

**État actuel : franchie.**

## Porte 2 — Sécurité moteur

- Stockfish 18, même binaire et mêmes paramètres pour toutes les lignes ;
- audit rapide 50 000 nœuds, puis audit publication 500 000 nœuds ;
- aucune ligne cœur au-delà de 50 cp de perte maximale sans justification approuvée ;
- contrôle particulier de la meilleure défense et de la continuation humaine des Noirs.

**État actuel : non exécutée en V1.**

## Porte 3 — Prédiction humaine Maia-3

- modèle final 79M ;
- Elo 1100, 1300, 1500, 1700, 1900, 2100 ;
- dix réponses par position ;
- probabilités de politique récupérées directement, pas déduites des rangs ;
- réponses évaluées ensuite avec Stockfish.

**État actuel : non exécutée.**

## Porte 4 — Validation empirique Lichess

- blitz et rapide séparés ;
- bandes de 200 Elo ;
- mois de découverte, validation et test distincts ;
- minimum 200 occurrences par position et 30 par réponse pour une affirmation forte ;
- intervalles de confiance pour les taux publiés ;
- vérification de la stabilité temporelle.

**État actuel : non exécutée.**

## Porte 5 — Pédagogie humaine

Cohortes minimales :

- 6 joueurs 1100–1399 ;
- 6 joueurs 1400–1699 ;
- 6 joueurs 1700–1999 ;
- 1 entraîneur ou joueur titré.

Mesurer : rappel après une semaine, confiance, temps de décision, qualité des trois coups suivant la sortie du cours, capacité à expliquer le plan et fréquence réelle d’obtention.

**État actuel : en attente.**

## Porte 6 — Chessable

- test d’import des huit PGN ;
- côté entraîné = Noir ;
- transpositions et coups alternatifs acceptés ;
- charge MoveTrainer contrôlée sur mobile et ordinateur ;
- relecture française finale ;
- description commerciale limitée aux preuves réellement obtenues.

**État actuel : en attente.**
