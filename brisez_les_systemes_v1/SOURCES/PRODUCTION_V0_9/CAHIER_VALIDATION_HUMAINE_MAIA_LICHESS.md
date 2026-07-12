# Cahier des charges — validation humaine par Elo et cadence

## Objectif

Mesurer si les coups sélectionnés créent réellement une asymétrie de difficulté contre des humains, sans confondre surprise ponctuelle, bruit statistique et valeur pédagogique durable.

## Données

- séparer blitz et rapide ;
- bandes Elo de 200 points : 1100–1299, 1300–1499, 1500–1699, 1700–1899, 1900–2099 ;
- exclure bullet, parties non classées et parties manifestement anormales ;
- conserver les horodatages de coups lorsqu’ils sont disponibles ;
- utiliser des périodes distinctes pour découverte, validation et test final.

## Mesures par position

1. fréquence d’obtention ;
2. fréquence du coup noir proposé avant publication du cours ;
3. distribution des réponses blanches ;
4. perte d’évaluation moyenne et médiane des réponses humaines ;
5. proportion de réponses dépassant 30, 60 et 100 centipions de perte ;
6. temps supplémentaire dépensé après le coup noir ;
7. score pratique, contrôlé par Elo et couleur ;
8. difficulté de notre continuation : perte moyenne des Noirs dans les trois coups suivants ;
9. robustesse si les Blancs trouvent la meilleure réponse ;
10. stabilité sur une période hors échantillon.

## Modèles

- Stockfish reste le filtre de solidité, jamais le modèle de comportement humain.
- Maia-2 peut fournir une distribution de coups conditionnée par le niveau.
- ChessMimic peut être testé pour des bandes de 100 Elo et pour la dimension temps de réflexion, mais doit être traité comme un système expérimental récent.
- Les prédictions d’un modèle ne remplacent pas les fréquences observées ; les deux doivent être comparées.

## Scores calculés

### Human Pressure Score empirique

Combiner, avec pondérations publiées : rareté du coup noir, probabilité d’une réponse imprécise, gravité de l’imprécision, coût en temps adverse et simplicité de notre continuation.

### Worst-Case Safety

Évaluation et jouabilité après la meilleure défense blanche. Un coup ne peut être “cœur du cours” si sa valeur dépend exclusivement d’une erreur.

### Learning Longevity

Évaluer par test humain si la règle apprise reste utile dans des positions voisines et au palier Elo supérieur.

## Précautions statistiques

- seuil minimal d’occurrences par position et par réponse ;
- intervalles de confiance, pas seulement pourcentages bruts ;
- correction du biais de sélection : les mêmes données ne peuvent servir à trouver et à confirmer le coup ;
- déduplication des transpositions ;
- contrôle du niveau des deux joueurs et de la cadence ;
- publication des lignes rejetées pour éviter le cherry-picking.

## Décision éditoriale

Chaque ligne reçoit un statut : CŒUR, ARME PRATIQUE, BONUS, À RÉVISER ou REJET. Les données humaines peuvent modifier la priorité d’apprentissage, mais ne doivent jamais sauver une ligne objectivement douteuse.
