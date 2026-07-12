# Sources, méthode et licences

## Maia-3

Projet officiel : `https://github.com/CSSLab/maia3`  
Révision épinglée pour l’adaptateur V1 : `1e13597c42d4858b7cfd7cfdae01e297263364b2`  
Modèles : collection MaiaChess sur Hugging Face.

Maia-3 sert à prédire les coups humains selon l’Elo. Ses sorties de politique sont des prédictions de modèle, pas des fréquences observées. Le script V1 utilise l’API directe pour accéder aux probabilités, car l’affichage UCI standard n’expose que le classement des candidats et les WDL.

## Lichess

Base ouverte : `https://database.lichess.org/`  
Les exports sont annoncés sous licence CC0. Le paquet ne redistribue aucun export de parties ; il fournit seulement un parseur et des schémas de résultats agrégés.

## Stockfish

Téléchargement officiel : `https://stockfishchess.org/download/`  
Stockfish est sous GPL. Le moteur et ses fichiers binaires ne sont pas inclus. Le paquet contient uniquement un script UCI et des résultats d’analyse séparés.

## Chessable

Le paquet produit des PGN annotés destinés à un cours privé puis à une vérification dans MoveTrainer. Il n’inclut aucun contenu copié d’un cours Chessable existant.

## Contenus pédagogiques tiers

Livres, vidéos et cours peuvent servir à étudier des critères généraux de qualité. Leur formulation, leurs annotations et leur architecture particulière ne doivent pas être reproduites. Les explications du cours doivent rester originales et chaque partie modèle ajoutée doit être sourcée.
