# Human Chess Lab

Dépôt de travail partagé pour concevoir, valider et publier le cours francophone **Brisez les systèmes !**

L’objectif est de sélectionner des idées d’ouverture :

- objectivement saines avec Stockfish 18 ;
- difficiles à résoudre pour des humains selon leur Elo avec Maia-3 ;
- confirmées, lorsque l’échantillon le permet, par des parties Lichess distinctes pour découverte, validation et test ;
- simples à comprendre, mémoriser et jouer en blitz ou en rapide.

## État actuel

La branche `agent/bootstrap-human-chess-lab-v1` contient le paquet complet **V1.0 RC1** sous une forme restaurable et vérifiée par SHA-256.

Aucune fréquence Maia-3 ou Lichess non mesurée n’est présentée comme un résultat. Les anciens audits moteur présents dans le paquet restent explicitement marqués comme historiques tant qu’ils ne sont pas reproduits.

## Restaurer le projet

### Linux et macOS

```bash
git switch agent/bootstrap-human-chess-lab-v1
bash bootstrap/restore_bundle.sh
cd brisez_les_systemes_v1
./LAB/run_static_qa.sh
```

### Windows PowerShell

```powershell
git switch agent/bootstrap-human-chess-lab-v1
powershell -ExecutionPolicy Bypass -File bootstrap/restore_bundle.ps1
cd brisez_les_systemes_v1
```

Les détails et le hash attendu sont documentés dans [`bootstrap/README.md`](bootstrap/README.md).

## Répartition du travail

### ChatGPT

- architecture du produit et du cours ;
- sélection éditoriale ;
- pédagogie française ;
- interprétation des audits ;
- relecture des résultats et des pull requests.

### Hermes

- installation et exécution des outils ;
- Stockfish 18, Maia-3 et extraction Lichess ;
- rapports reproductibles ;
- corrections techniques ciblées ;
- Git, commits et pull requests.

## Workflow Git recommandé

1. restaurer la RC1 depuis la branche de bootstrap ;
2. créer une branche `work/empirical-validation-v1` ;
3. exécuter les phases décrites dans `brisez_les_systemes_v1/LAB/README_LAB.md` ;
4. produire les rapports sans modifier immédiatement les 40 idées ;
5. ouvrir une pull request brouillon ;
6. effectuer une validation éditoriale séparée avant toute fusion ou publication.

Ne jamais utiliser les moteurs ou modèles pour assister une partie en cours. Le laboratoire sert uniquement à la préparation, à l’analyse hors ligne et à la création pédagogique.
