# Méthodologie, sources et licences

## Méthode

Les lignes sont construites à partir de principes d’ouverture généraux, d’analyse originale et d’un audit Stockfish. Les commentaires pédagogiques sont originaux. Les coups de parties d’échecs sont des faits de jeu ; aucune annotation, transcription de vidéo ou structure de cours tiers n’est reproduite.

## Outils

- Stockfish 18 via UCI pour la vérification des coups imposés et la prolongation critique des lignes ;
- audit approfondi distinct des 20 coups signature à 200 000 nœuds, sans ligne classée “à revoir” ;
- python-chess pour la validation légale et l’export PGN ;
- manifeste prévu pour Maia-2/ChessMimic ou une base Lichess filtrée par Elo et cadence.

## Statut Maia / modèles humains

Aucune inférence Maia n’est incluse dans cette livraison. Les poids n’étaient pas disponibles localement dans l’environnement de production. Le cours évite donc toute affirmation chiffrée sur la probabilité d’une erreur humaine. Le manifeste permet d’ajouter cette couche sans changer le contenu PGN.

## Usage de ressources pédagogiques tierces

Les cours, vidéos et livres peuvent servir à établir des critères de qualité — clarté des plans, progression, exemples contrastifs — mais leur texte et leur organisation spécifique ne doivent pas être copiés. Toute partie modèle ajoutée ultérieurement devra être sourcée et annotée de façon originale.

## Licence moteur

Stockfish est distribué sous GPL. Le cours ne redistribue pas le moteur ni son réseau : il contient uniquement des résultats d’analyse et des fichiers PGN originaux.
