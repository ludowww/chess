# Brisez les systèmes !

## Un répertoire noir anti-Londres, Jobava, Colle, Torre, Veresov, Stonewall et Blackmar-Diemer

**Version :** 0.9.0-beta-professionnelle  
**Public :** joueurs en ligne environ 1100–1999, surtout blitz et rapide  
**Promesse :** jouer des coups objectivement sains qui retirent à l’adversaire le confort de son système, tout en conservant des plans simples pour les Noirs.

---

## 1. Ce que couvre le cours

Le cours répond à **1.d4 sans 2.c4 principal** par un répertoire cohérent fondé sur `1...d5`, la rupture `...c5`, le développement actif du fou c8 et des questions immédiates à la structure blanche. Il couvre :

- le Londres classique et ses ordres de coups ;
- le Jobava-Londres ;
- le Colle-Koltanowski et le Colle-Zukertort ;
- la Torre ;
- le Veresov et le pseudo-Trompowsky ;
- le Stonewall ;
- le Blackmar-Diemer.

Le gambit dame avec `2.c4`, la Catalane et les grandes Indiennes ne font pas partie de ce produit : les inclure diluerait la promesse et multiplierait inutilement la charge de mémorisation.

## 2. La philosophie anti-humaine

Ce répertoire ne choisit pas un coup simplement parce qu’il est rare. Chaque décision doit satisfaire quatre conditions :

1. **Solidité** : la ligne imposée reste dans une zone objectivement saine au moteur.
2. **Asymétrie de difficulté** : notre plan doit être plus simple que la réponse adverse.
3. **Rupture d’automatisme** : le coup doit forcer une décision réelle à un joueur habitué à dérouler un système.
4. **Valeur durable** : même connu, le coup doit mener à une position jouable et instructive.

Les notes “surprise”, “charge adverse”, “simplicité” et “longévité” du fichier d’index sont des **jugements éditoriaux**, jamais présentés comme des statistiques. Les probabilités par Elo sont réservées à une validation ultérieure avec une base de parties filtrée et un modèle humain.

## 3. Les douze règles mémoire

### Règle 1 — Le système se frappe avant d’être terminé

Quand les Blancs ont joué `Bf4`, `Bg5`, `e3` ou `Nc3` sans encore avoir stabilisé le centre, le premier réflexe est `...c5`. Nous ne cherchons pas à “réfuter” le système ; nous l’empêchons de devenir automatique.

### Règle 2 — `...Qb6` pose deux questions avec une seule pièce

Dans le Londres, la dame noire vise d4 et b2. La valeur pratique vient du dilemme : défendre b2, maintenir d4, finir le développement ou échanger les dames. Les Blancs ne peuvent pas tout faire en un coup.

### Règle 3 — Après `Qb3`, pense `...c4`

L’échange de dames n’est pas toujours une simplification favorable aux Blancs. `...c4` gagne un tempo, fixe la structure et, après `Qxb6 axb6`, ouvre la colonne a. La structure noire est asymétrique mais active.

### Règle 4 — Ne prends b2 que si tu connais la sortie

`...Qxb2` est recommandé uniquement dans des positions auditées. La question n’est pas “la dame risque-t-elle d’être chassée ?”, mais “où sort-elle après Rb1 ?”. Les cases c3, a3, a5 ou a6 doivent être identifiées avant la prise.

### Règle 5 — `...Nh5` est un coup de temps, pas une obsession de paire de fous

Le but est d’obtenir une concession : recul du fou, structure h ouverte, perte de temps ou abandon du contrôle de e5. Si la chasse n’est pas utile, on clarifie d4 et on développe.

### Règle 6 — Contre le Jobava, `Nb5` appelle souvent `...Qa5+`

Le cavalier c3 ne peut plus interposer sur l’échec. Ce motif transforme la menace Nc7+ en perte de temps, parfois en perte de pion. Il faut le reconnaître avant de calculer des variantes longues.

### Règle 7 — Une prise en c5 avec un cavalier c3 peut autoriser `...d4`

Dans le Jobava et le Veresov, `dxc5` est souvent rencontré par `...d4!`. Les Noirs ne récupèrent pas le pion tout de suite : ils chassent la pièce, gagnent de l’espace, puis récupèrent avec développement.

### Règle 8 — Contre le Colle, le fou c8 sort avant `...e6`

`...Bf5` retire au Colle son plan automatique e4. Le fou contrôle e4, peut s’échanger contre Bd3 et permet aux Noirs de choisir ensuite entre `...c6` et `...c5`.

### Règle 9 — Contre la Torre, la case e4 appartient au cavalier

Après `Bg5`, `...Ne4` refuse le clouage confortable. Si le fou recule plusieurs fois, chaque recul est transformé en rupture centrale ou en restriction par `...h5` et `...f6`.

### Règle 10 — Une structure laide peut être active

Après `Bxf6 gxf6`, les Noirs gagnent la paire de fous, la colonne g et le contrôle de e5. On ne roque pas automatiquement court : le roi choisit son abri après avoir vu le plan blanc.

### Règle 11 — Contre le Stonewall, coupe le fou d3 par `...c4`

Le Stonewall dépend de l’activité du fou d3 et de la rupture e4. `...c4` réduit la diagonale, gagne de l’espace et déplace le jeu vers l’aile-dame.

### Règle 12 — Contre un gambit, développe avant de défendre le pion

Dans le Blackmar-Diemer, les Noirs acceptent le pion, développent le fou c8, consolident f7 et roquent. La priorité n’est pas de rester un pion de plus à tout prix, mais d’échanger les pièces attaquantes.

---

## 4. Parcours d’apprentissage par niveau

### Piste Essentiel — environ 1100–1399

Apprendre le fichier `00_demarrage_rapide_24_lignes.pgn`. L’objectif est de mémoriser les douze règles, pas toutes les sous-variantes. Les positions prioritaires sont `...Qb6`, `...c4`, `...Qa5+`, `...d4`, `...Ne4`, `...Bf5` et l’acceptation du Blackmar-Diemer.

### Piste Club — environ 1400–1699

Ajouter toutes les lignes marquées **Club**. Le travail se déplace vers les structures : colonne a après `axb6`, colonne c semi-ouverte, cases e4/e5, choix de reprise en d4 et itinéraires de sortie de la dame.

### Piste Avancé — environ 1700–1999

Ajouter les lignes **Avancé**, puis refaire le cours par positions aléatoires. À ce niveau, la valeur vient moins du piège que de la capacité à obtenir une position rare, saine et comprise plus profondément que l’adversaire.

---

## 5. Chapitre Londres : le dilemme b2–d4

Le noyau du cours est :

`1.d4 d5 2.Nf3 Nf6 3.Bf4 c5 4.e3 Nc6 5.c3 Qb6!`

La dame noire ne “sort pas trop tôt” : elle attaque deux éléments insuffisamment coordonnés. Les réponses blanches se classent en quatre familles.

**Échange par Qb3.** Répondre `...c4`. Après échange, la colonne a et la poussée `...b5` donnent aux Noirs un plan plus clair que ne le suggère l’apparence des pions doublés.

**Défense par Qc1/Qc2.** Clarifier d4 ou jouer `...Nh5`. La dame blanche a perdu du temps et gêne souvent une tour ou un fou.

**Défense par b3.** Changer de cible : `...Bg4`, pression sur f3 et d4, puis `...e6`.

**Ignorer la menace.** `Bd3`, `h3`, `Nbd2` ou `dxc5` peuvent permettre `...Qxb2`. La prise n’est jouée que lorsqu’une sortie concrète a été vérifiée.

### Position-cible du chapitre

Les Noirs veulent une des trois positions suivantes :

- finale sans dames avec colonne a et expansion `...b5` ;
- milieu de jeu avec colonne c semi-ouverte et fou développé en f5 ;
- gain de pion sur b2 avec dame sortie par c3/a5 et développement ensuite prioritaire.

---

## 6. Chapitre Jobava : retourner la menace

Le noyau est :

`1.d4 d5 2.Nc3 Nf6 3.Bf4 c5!`

Le Jobava cherche Nb5, e4 et parfois h4. Notre réponse n’est pas défensive. Nous ouvrons d4 et utilisons deux motifs : `...Qa5+` contre Nb5 et `...d4` après dxc5.

Le test pratique est simple : avant chaque coup noir, demander si le cavalier c3 peut encore bloquer un échec en a5. S’il est parti en b5, la réponse est non. Avant de récupérer un pion c5, demander si `...d4` gagne un tempo. Si oui, le tempo vaut souvent plus que le pion immédiat.

---

## 7. Chapitre Colle/Zukertort : retirer le rêve e4

Le Colle n’est dangereux que si les Noirs coopèrent en enfermant leur fou et en laissant e4 arriver sans coût. `...Bf5` change la géométrie : e4 est contrôlé, Bd3 peut être échangé et le développement noir devient naturel.

Contre le Zukertort, la règle est différente : jouer `...c5` avant que Bb2–Bd3–Nbd2–O-O n’assemble une attaque. Les Noirs n’ont pas besoin de créer une faiblesse ; ils réduisent le temps disponible pour le plan blanc.

---

## 8. Chapitre Torre : transformer le clouage en cible

Après `3.Bg5`, `...Ne4` place une pièce sur la case que le fou a cessé de contrôler efficacement. Si le fou va en f4, on joue `...c5` et `...Qb6`. S’il va en h4, `...h5` prépare une cage. Si les Blancs jouent Nbd2 ou c4 sans précaution, `...Nxg5` suivi de `...e5` gagne le centre.

La poussée `...f6` n’est pas une permission générale d’affaiblir le roi. Elle est jouée lorsque trois conditions sont réunies : le fou perd un tempo, le centre est contrôlé et l’ouverture de la diagonale e7–h4 ne donne pas d’échec dangereux.

---

## 9. Chapitre Veresov et pseudo-Trompowsky

Contre le Veresov, `...c5` arrive avant e4. Les motifs du Jobava se répètent, ce qui réduit la mémoire : `dxc5` peut rencontrer `...d4`, f3 peut rencontrer `...cxd4`, et e4 doit être vérifié tactiquement.

Contre `2.Bg5`, `...h6` pose une question avant de développer le cavalier. Les retraits Bh4, Bf4 et Be3 mènent tous à `...c5`, mais avec une concession blanche différente. Le sacrifice Bxh6 est accepté.

---

## 10. Chapitre Stonewall et Blackmar-Diemer

Le Stonewall veut fermer le centre à son avantage et attaquer le roi. `...c4` renverse la logique : le centre est fermé de façon à réduire le fou d3, puis les Noirs gagnent de l’espace par `...b5`.

Contre le Blackmar-Diemer, le cours accepte le gambit. Le plan est répétitif : `...exf3`, développement du fou c8, protection de f7 par `...e6` ou fianchetto, roque, puis échanges. La ligne `5.Qxf3? Qxd4` illustre le danger d’une attaque qui oublie son centre.

---

## 11. Méthode d’étude dans MoveTrainer

Pour chaque ligne :

1. lire uniquement l’objectif et le repère mémoire ;
2. jouer la ligne une première fois avec les commentaires ;
3. rejouer sans commentaires ;
4. expliquer à voix haute pourquoi le coup noir est facile pour nous et difficile pour l’adversaire ;
5. après cinq lignes, jouer une partie rapide et rechercher la position, sans forcer artificiellement la variante.

Une erreur de mémoire qui conserve le bon plan est moins grave qu’un coup mémorisé sans compréhension. Le test final n’est pas de réciter quinze coups : c’est de trouver le bon plan lorsque l’adversaire dévie au sixième.

---

## 12. Contrôle qualité actuel

- **88 lignes de répertoire** réparties en **7 fichiers de chapitre**, plus **20 positions de test**.
- Audit des coups noirs imposés avec Stockfish 18 ; audit approfondi des 20 coups signature à 200 000 nœuds : 19 grades A, 1 grade B, aucune ligne à revoir. Synthèse de l’audit rapide des préfixes : {'A': 82, 'B': 6}.
- Aucun taux de victoire, taux d’erreur ou coût en secondes n’est inventé.
- Un manifeste de validation humaine par bandes de 200 Elo est fourni.
- Les commentaires sont originaux et ne reproduisent pas les annotations de cours tiers.

La version est complète sur son périmètre éditorial, mais reste une **bêta professionnelle** tant que trois contrôles externes ne sont pas terminés : validation par un entraîneur fort/titré, test par joueurs des trois paliers, et mesure Lichess/Maia ou ChessMimic sur un échantillon hors entraînement.
