# Human Chess Lab — mode d’emploi

## But

Le laboratoire doit répondre à quatre questions distinctes :

1. **Stockfish** — le coup est-il objectivement sain ?
2. **Maia-3** — quelles réponses un humain de ce niveau est-il susceptible de choisir ?
3. **Lichess** — ces réactions apparaissent-elles réellement, avec quelle fréquence et dans quelle cadence ?
4. **Édition pédagogique** — notre plan est-il simple, mémorisable et durable ?

Les couches ne doivent jamais être confondues. Une prédiction Maia-3 n’est pas une fréquence observée. Une fréquence Lichess élevée ne sauve pas une ligne réfutable. Une bonne évaluation Stockfish ne rend pas automatiquement une ligne enseignable.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate       # Windows : .venv\\Scripts\\activate
pip install -r LAB/requirements.txt
```

Installer ensuite Maia-3 depuis la révision épinglée utilisée pour l’adaptateur direct :

```bash
pip install 'git+https://github.com/CSSLab/maia3.git@1e13597c42d4858b7cfd7cfdae01e297263364b2'
```

Installer séparément Stockfish 18 pour la plateforme concernée et conserver le chemin du binaire. Le moteur n’est pas redistribué dans ce paquet.

## Pourquoi l’adaptateur Maia-3 est direct

L’interface UCI officielle classe les candidats par probabilité de politique et fournit leurs WDL, mais n’imprime pas la probabilité de politique elle-même dans les lignes UCI. `maia3_profile.py` utilise donc l’API Python interne de la révision épinglée afin de récupérer le champ `policy`. Il échoue explicitement si cette API change : il ne transforme jamais un rang MultiPV en fausse probabilité.

## 1. Contrôle statique

```bash
./LAB/run_static_qa.sh
```

## 2. Audit Stockfish reproductible

```bash
python LAB/scripts/stockfish_audit.py \
  --pgn PGN/99_cours_v1_core_40.pgn \
  --manifest DATA/core_40_index.csv \
  --engine /chemin/vers/stockfish \
  --nodes 500000 \
  --output DATA/stockfish_v1_500k.csv
```

Le script compare chaque coup noir de la ligne au meilleur choix trouvé sous la même limite de nœuds.

## 3. Profils Maia-3

Premier test CPU :

```bash
python LAB/scripts/maia3_profile.py \
  --manifest DATA/core_40_index.csv \
  --model maia3-5m \
  --device cpu \
  --multipv 10 \
  --output DATA/maia3_5m_probe.csv
```

Analyse finale recommandée :

```bash
python LAB/scripts/maia3_profile.py \
  --manifest DATA/core_40_index.csv \
  --model maia3-79m \
  --device cuda \
  --multipv 10 \
  --output DATA/maia3_79m_profiles.csv
```

Niveaux par défaut : 1100, 1300, 1500, 1700, 1900 et 2100.

## 4. Données Lichess

Télécharger des mois distincts pour découverte, validation et test, puis :

```bash
python LAB/scripts/lichess_extract.py \
  /data/lichess_db_standard_rated_2026-01.pgn.zst \
  /data/lichess_db_standard_rated_2026-02.pgn.zst \
  --manifest DATA/core_40_index.csv \
  --split discovery \
  --output DATA/lichess_discovery.csv
```

Répéter avec d’autres mois pour `validation` et `test`. Ne jamais réutiliser les mêmes mois pour sélectionner puis confirmer une idée.

Le script mesure deux positions :

- `before_key` : fréquence réelle de notre coup-clé ;
- `after_key` : distribution des réponses adverses.

## 5. Évaluer les réponses humaines avec Stockfish

Pour Maia-3 :

```bash
python LAB/scripts/evaluate_responses.py \
  --distribution DATA/maia3_79m_profiles.csv \
  --manifest DATA/core_40_index.csv \
  --engine /chemin/vers/stockfish \
  --output DATA/maia3_79m_evaluated.csv
```

Pour Lichess :

```bash
python LAB/scripts/evaluate_responses.py \
  --distribution DATA/lichess_test.csv \
  --manifest DATA/core_40_index.csv \
  --engine /chemin/vers/stockfish \
  --output DATA/lichess_test_evaluated.csv
```

## 6. Scorecards

```bash
python LAB/scripts/score_candidates.py \
  --manifest DATA/core_40_index.csv \
  --stockfish DATA/stockfish_v1_500k.csv \
  --maia-evaluated DATA/maia3_79m_evaluated.csv \
  --lichess-distribution DATA/lichess_test.csv \
  --lichess-evaluated DATA/lichess_test_evaluated.csv \
  --output DATA/scorecards_validated.csv
```

Le score composite reste vide tant que les couches moteur, Maia et Lichess ne sont pas toutes présentes. C’est une protection contre les résultats séduisants mais fictifs.

## Limites connues

- Maia-3 prédit un comportement moyen conditionné par Elo ; il ne connaît pas la préparation individuelle de l’adversaire.
- Les bases Lichess subissent des biais de population, de plateforme, de période et de sélection.
- Les temps de réflexion ne sont pas exploités par le parseur V1 ; ils pourront être ajoutés depuis les commentaires `%clk`.
- Les transpositions peuvent regrouper plusieurs histoires de partie dans la même FEN ; Maia-3 doit idéalement recevoir l’historique UCI lorsque celui-ci est disponible.
- Le score final reste un outil de tri, jamais un substitut à une décision éditoriale et à une relecture forte.
