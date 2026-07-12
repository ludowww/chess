# Brisez les systèmes ! — V1 Human Chess Lab

## Répertoire noir anti-systèmes, organisé par erreurs humaines

**Version :** 1.0.0-rc1  
**Public :** environ 1100–2000 Elo, blitz et rapide  
**Périmètre :** réponses à `1.d4` sans `2.c4` principal  
**Statut :** cours complet en contenu, candidat à validation — pas encore publiable comme produit “prouvé par les données”.

## Promesse

Ce cours ne demande pas : « quel est le coup le plus théorique ? » Il demande : **quel coup sain crée une décision difficile pour l’adversaire tout en laissant un plan simple aux Noirs ?** Stockfish contrôle la sécurité objective. Maia‑3 modélise les réponses humaines par niveau. Les parties Lichess doivent confirmer les fréquences réelles sur des périodes séparées. La pédagogie décide enfin ce qui mérite d’être appris.

## Architecture du produit

- **20 lignes essentielles** : mise en route rapide.
- **40 idées centrales** : cinq idées dans chacune des huit familles d’erreurs.
- **48 lignes de bibliothèque** : conservées pour recherche, mais sorties du parcours principal tant qu’elles ne gagnent pas leur place.
- **Aucun taux humain inventé** : les colonnes Maia‑3 et Lichess restent vides avant exécution réelle.

## Doctrine de sélection

Une idée ne passe en publication que si elle franchit cinq portes :

1. **Saine** : perte moteur sous le seuil éditorial et évaluation stable.
2. **Asymétrique** : notre plan est plus facile que la défense adverse.
3. **Atteignable** : la position apparaît assez souvent dans la pratique.
4. **Humaine** : Maia‑3 et les parties réelles montrent une difficulté au palier visé.
5. **Enseignable** : une phrase mémoire et une ligne de sécurité suffisent à guider le joueur.

## Comment étudier

Commencer par `PGN/00_parcours_essentiel_20.pgn`. Pour chaque ligne, réciter : **le déclencheur, le coup, la croyance adverse, le plan noir, la sécurité si l’adversaire connaît**. Ajouter ensuite un chapitre de biais à la fois. La bibliothèque de 88 lignes n’est pas un devoir : c’est un réservoir éditorial.

# B1 — Pilotage automatique

## Frapper avant que le système ne soit terminé

**Croyance exploitée :** Je peux dérouler mon schéma de développement sans regarder ce que fait l’adversaire.

**Compétence durable :** Une rupture centrale jouée au bon moment vaut plus qu’un développement passif et symétrique.

## B1.1 — ORD-01 — 2.Bf4 : ...c5 puis le clouage ...Bg4

**Déclencheur :** `1. d4 d5 2. Bf4 c5 3. e3 Nc6 4. Nf3 Bg4`  
**Coup-clé :** `Bg4`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Londres — ordres de coups

### Ce que l’humain croit
Sans c3, la dame noire n’a pas besoin de sortir tôt ; le clouage ralentit le développement naturel.

### Ce que le coup change
Frapper le centre puis développer avec un clouage avant de sortir la dame.

### Plan simple pour les Noirs
Après Be2, choisir entre ...Bxe2 et ...e6 ; après h3, décider Bh5 ou Bf5.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Sans c3, développe d’abord ; avec c3, ...Qb6 devient plus fort.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **19 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B1.2 — ORD-02 — 2.Bf4 et 3.c3 : revenir au plan ...Nc6

**Déclencheur :** `1. d4 d5 2. Bf4 c5 3. c3 Nc6 4. e3 Nf6 5. Nf3 Qb6`  
**Coup-clé :** `Qb6`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Londres — ordres de coups

### Ce que l’humain croit
c3 semble sécuriser d4 mais retire la meilleure case au cavalier b1.

### Ce que le coup change
Retrouver le noyau du répertoire par transposition.

### Plan simple pour les Noirs
Attaquer b2 et d4 ; utiliser ...Bf5 si la dame recule.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> c3 protège d4 une fois et affaiblit b2 pour longtemps.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **19 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B1.3 — COL-01 — 3.e3 : sortir le fou avec ...Bf5

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. e3 Bf5 4. Bd3 e6`  
**Coup-clé :** `e6`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Colle et Zukertort

### Ce que l’humain croit
Le Colle compte sur un Noir qui joue automatiquement ...e6 puis subit e4.

### Ce que le coup change
Développer le fou c8 avant de fermer sa diagonale.

### Plan simple pour les Noirs
Après Bxf5 exf5, utiliser la colonne e et contrôler e4.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Contre le Colle, le fou c8 sort avant le pion e.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **21 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B1.4 — COL-10 — Zukertort : frapper par ...c5

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. e3 e6 4. b3 c5 5. Bb2 Nc6`  
**Coup-clé :** `Nc6`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Colle et Zukertort

### Ce que l’humain croit
Le plan blanc est lent et suppose une position fermée.

### Ce que le coup change
Occuper l’espace avant que Bb2 et Bd3 ne construisent une attaque.

### Plan simple pour les Noirs
Jouer ...Bd6, ...O-O et parfois ...cxd4 pour isoler d4.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Le Zukertort aime le temps : enlève-lui du temps avec ...c5.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **1 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B1.5 — VER-01 — 3...c5 : attaquer d4 immédiatement

**Déclencheur :** `1. d4 d5 2. Nc3 Nf6 3. Bg5 c5 4. e3 e6`  
**Coup-clé :** `e6`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Veresov et pseudo-Trompowsky

### Ce que l’humain croit
Le Veresov veut e4 sans rencontrer de tension centrale.

### Ce que le coup change
Refuser une position fermée et préparer ...Nc6.

### Plan simple pour les Noirs
Développer ...Nc6, ...Be7 et décider entre ...cxd4 et ...Be7.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Contre Nc3+Bg5, la réponse est ...c5 avant e4.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

# B2 — Double cible et surcharge

## Faire travailler une pièce à deux tâches incompatibles

**Croyance exploitée :** Un seul coup de défense suffit à remettre mon système sur ses rails.

**Compétence durable :** La dame, le pion d4 et le pion b2 ne peuvent pas toujours être protégés en même temps.

## B2.1 — LON-02 — La dame recule en c2 : ...Bf5

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. e3 Nc6 5. c3 Qb6 6. Qb3 c4 7. Qc2 Bf5`  
**Coup-clé :** `Bf5`  
**Niveau :** Club  
**Famille d’ouverture :** Londres — noyau ...Qb6

### Ce que l’humain croit
Le recul Qc2 paraît naturel mais autorise un second gain de temps.

### Ce que le coup change
Développer avec tempo sur la dame et obtenir une version améliorée du développement noir.

### Plan simple pour les Noirs
Après ...Bf5, développer ...e6, ...Be7 et choisir entre ...Nh5 et ...e5.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Une dame déplacée deux fois doit être interrogée une troisième fois.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B2.2 — LON-04 — Qc1 et reprise par le pion e

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. e3 Nc6 5. c3 Qb6 6. Qc1 cxd4 7. exd4 Bf5`  
**Coup-clé :** `Bf5`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Londres — noyau ...Qb6

### Ce que l’humain croit
Qc1 défend b2 mais enferme la tour a1 et laisse les Noirs gagner l’initiative de développement.

### Ce que le coup change
Clarifier le centre puis développer le fou avant ...e6.

### Plan simple pour les Noirs
Mettre le fou en f5, jouer ...e6 et exploiter la colonne c semi-ouverte.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Quand la dame retourne en c1, ouvre la colonne c avant qu’elle ne ressorte.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **15 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B2.3 — LON-09 — b3 protège b2 : développer avec ...Bg4

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. e3 Nc6 5. c3 Qb6 6. b3 Bg4`  
**Coup-clé :** `Bg4`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Londres — noyau ...Qb6

### Ce que l’humain croit
b3 règle un problème immédiat mais affaiblit c3 et ralentit le développement du cavalier b1.

### Ce que le coup change
Répondre à une concession de case sombre par un développement actif.

### Plan simple pour les Noirs
Mettre la pression sur f3, jouer ...e6 et échanger en d4 au bon moment.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Quand b2 est sauvé par b3, change de cible : f3 et d4.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **2 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B2.4 — JOB-12 — 4.Nb1 : la pression ...Qb6

**Déclencheur :** `1. d4 d5 2. Nc3 Nf6 3. Bf4 c5 4. Nb1 Qb6`  
**Coup-clé :** `Qb6`  
**Niveau :** Club  
**Famille d’ouverture :** Jobava

### Ce que l’humain croit
Le cavalier recule pour éviter les tactiques, mais le développement blanc recommence à zéro.

### Ce que le coup change
Punir le retrait du cavalier par une double attaque sur b2 et d4.

### Plan simple pour les Noirs
Prendre b2 si les cases de sortie sont claires ; sinon développer ...Nc6.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Un retrait au premier rang autorise la dame à entrer.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **5 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B2.5 — TOR-10 — Bf4 puis ...Qb6 : double pression

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bg5 Ne4 4. Bf4 c5 5. e3 Qb6`  
**Coup-clé :** `Qb6`  
**Niveau :** Avancé  
**Famille d’ouverture :** Torre

### Ce que l’humain croit
Les Blancs ont replacé le fou comme au Londres mais ont perdu un tempo.

### Ce que le coup change
Combiner l’avant-poste e4 avec la cible b2.

### Plan simple pour les Noirs
Jouer ...Nc6 et prendre b2 si la dame dispose d’une sortie.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Une Torre qui recule en f4 est un Londres avec un tempo de moins.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **3 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

# B3 — Simplification trompeuse

## Accepter une structure imparfaite mais active

**Croyance exploitée :** Échanger les dames ou créer des pions doublés neutralise automatiquement l’initiative.

**Compétence durable :** Une colonne ouverte, de l’espace et des tempos peuvent valoir davantage qu’une structure esthétique.

## B3.1 — LON-01 — La dame blanche s’échange : ...c4!

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. e3 Nc6 5. c3 Qb6 6. Qb3 c4 7. Qxb6 axb6`  
**Coup-clé :** `axb6`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Londres — noyau ...Qb6

### Ce que l’humain croit
Le joueur du Londres pense neutraliser la pression par un échange de dames ; il sous-estime la structure active des Noirs.

### Ce que le coup change
Fermer le centre avec gain de temps et accepter les pions doublés pour ouvrir la colonne a.

### Plan simple pour les Noirs
Jouer ...b5, ...Bf5 et utiliser la colonne a ; le fou f4 manque souvent de bonnes cases.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Qb3 ? Répondre c4 ; après l’échange, la colonne a paie les pions doublés.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B3.2 — LON-03 — La finale asymétrique : le plan ...b5

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. e3 Nc6 5. c3 Qb6 6. Qb3 c4 7. Qxb6 axb6 8. Nbd2 b5`  
**Coup-clé :** `b5`  
**Niveau :** Avancé  
**Famille d’ouverture :** Londres — noyau ...Qb6

### Ce que l’humain croit
Les Blancs évaluent souvent les pions b6-b7 comme faibles sans voir la poussée ...b5-b4.

### Ce que le coup change
Transformer une faiblesse statique apparente en majorité d’espace et colonne ouverte.

### Plan simple pour les Noirs
Fixer l’aile-dame, développer le fou c8 en f5 et doubler les tours sur la colonne a.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Les pions doublés ne sont faibles que s’ils ne bougent pas et si la colonne ouverte ne sert à rien.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B3.3 — LON-05 — Qc1 et reprise par le pion c

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. e3 Nc6 5. c3 Qb6 6. Qc1 cxd4 7. cxd4 Bf5`  
**Coup-clé :** `Bf5`  
**Niveau :** Club  
**Famille d’ouverture :** Londres — noyau ...Qb6

### Ce que l’humain croit
La reprise cxd4 paraît saine mais laisse c3 vide et facilite ...Nb4.

### Ce que le coup change
Forcer une structure de Carlsbad inversée où les Noirs ont déjà développé activement.

### Plan simple pour les Noirs
Développer ...e6, viser b4 et mettre une tour en c8.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Après cxd4, la case b4 devient une vraie destination.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **15 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B3.4 — JOB-11 — 4.Bxb8 : reprendre avec la tour

**Déclencheur :** `1. d4 d5 2. Nc3 Nf6 3. Bf4 c5 4. Bxb8 Rxb8`  
**Coup-clé :** `Rxb8`  
**Niveau :** Club  
**Famille d’ouverture :** Jobava

### Ce que l’humain croit
Les Blancs pensent abîmer la coordination noire en échangeant le fou contre le cavalier.

### Ce que le coup change
Accepter une structure inhabituelle pour activer la tour sur la colonne b.

### Plan simple pour les Noirs
Jouer ...a6, ...e6 et utiliser b2 comme cible de long terme.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Une tour développée gratuitement peut valoir plus que le droit de roquer côté dame.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B3.5 — VER-05 — 4.Bxf6 : reprendre du pion g

**Déclencheur :** `1. d4 d5 2. Nc3 Nf6 3. Bg5 c5 4. Bxf6 gxf6`  
**Coup-clé :** `gxf6`  
**Niveau :** Club  
**Famille d’ouverture :** Veresov et pseudo-Trompowsky

### Ce que l’humain croit
Les Blancs appliquent la règle “abîmer les pions du roque” sans regarder que le roi noir peut roquer long ou rester au centre.

### Ce que le coup change
Accepter la structure pour obtenir la colonne g et un centre mobile.

### Plan simple pour les Noirs
Jouer ...cxd4, ...e6 et utiliser la paire de fous.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Les pions doublés g contrôlent e5 et ouvrent la colonne g.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

# B4 — Le pion prétendument gratuit

## Calculer la sortie avant la prise

**Croyance exploitée :** Une dame exposée ne peut pas prendre un pion d’aile sans se faire enfermer.

**Compétence durable :** La prise n’est correcte que si l’itinéraire de sortie et le développement suivant sont connus.

## B4.1 — LON-10 — Le pion c5 “gratuit” : ...Qxb2!

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. e3 Nc6 5. c3 Qb6 6. dxc5 Qxb2 7. Nbd2 Qxc3`  
**Coup-clé :** `Qxc3`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Londres — noyau ...Qb6

### Ce que l’humain croit
Le joueur du système voit un pion en c5 et oublie que sa tour a1 est encore enfermée.

### Ce que le coup change
Exploiter la surcharge de la dame blanche : elle ne peut défendre c5, b2 et le développement.

### Plan simple pour les Noirs
Rentrer par a5 ou c3, puis développer ; ne pas collectionner les pions sans voie de sortie.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Avant de prendre c5, compte b2 — deux fois.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B4.2 — LON-11 — Nbd2 laisse b2 : la route de sortie ...Qxc3

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. e3 Nc6 5. c3 Qb6 6. Nbd2 Qxb2 7. Rb1 Qxc3`  
**Coup-clé :** `Qxc3`  
**Niveau :** Club  
**Famille d’ouverture :** Londres — noyau ...Qb6

### Ce que l’humain croit
Rb1 ressemble à un gain de dame, mais c3 devient la case d’évacuation.

### Ce que le coup change
Prendre b2 seulement lorsque la dame dispose d’une case de fuite concrète.

### Plan simple pour les Noirs
Après ...Qxc3, répondre au développement par ...Bd7 ou ...cxd4 et ramener la dame.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Une dame n’est pas piégée si elle peut sortir par la case que le pion c vient de quitter.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **4 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B4.3 — LON-12 — Bd3 oublie b2

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. e3 Nc6 5. c3 Qb6 6. Bd3 Qxb2 7. Nbd2 Qxc3`  
**Coup-clé :** `Qxc3`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Londres — noyau ...Qb6

### Ce que l’humain croit
Bd3 est le coup “du système”, mais la position exige d’abord de traiter b2.

### Ce que le coup change
Punir un développement automatique qui ne répond pas à la menace immédiate.

### Plan simple pour les Noirs
Après le gain de pion, neutraliser e4 et finir le développement sans précipitation.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Un coup normal peut être une gaffe s’il ignore une question concrète.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B4.4 — LON-15 — Qa4 ne sauve pas b2 : ...Qxb2

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. e3 Nc6 5. c3 Qb6 6. Qa4 Qxb2`  
**Coup-clé :** `Qxb2`  
**Niveau :** Avancé  
**Famille d’ouverture :** Londres — noyau ...Qb6

### Ce que l’humain croit
Qa4 donne une impression d’activité, mais la dame blanche ne protège toujours pas son aile-dame.

### Ce que le coup change
Vérifier concrètement la cible b2 au lieu de répondre automatiquement au pseudo-clouage.

### Plan simple pour les Noirs
Après ...Qxb2, préparer ...Bd7 ou ...a6 et identifier la sortie avant Rb1.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Une dame active ne protège pas automatiquement les pions qu’elle a quittés.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B4.5 — PST-04 — 3.Bxh6? : accepter le sacrifice

**Déclencheur :** `1. d4 d5 2. Bg5 h6 3. Bxh6 Rxh6`  
**Coup-clé :** `Rxh6`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Veresov et pseudo-Trompowsky

### Ce que l’humain croit
Le joueur pense empêcher le roque et gagner deux pions pour le fou.

### Ce que le coup change
Reconnaître un sacrifice visuellement tentant mais insuffisant.

### Plan simple pour les Noirs
Développer ...Nf6, ...c5 et utiliser la tour active h6.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Deux pions ne valent pas un fou ; la tour h6 peut rentrer par h8.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **23 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

# B5 — Peur et sur-réaction

## Faire perdre un tempo au fou du système

**Croyance exploitée :** Je dois conserver mon fou à tout prix ou répondre immédiatement à une menace visuelle.

**Compétence durable :** Le harcèlement n’a de valeur que s’il provoque une concession concrète et laisse un plan simple.

## B5.1 — LON-06 — Qc2 : poser la question avec ...Nh5

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. e3 Nc6 5. c3 Qb6 6. Qc2 Nh5 7. Bg3 Nxg3 8. hxg3`  
**Coup-clé :** `hxg3`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Londres — noyau ...Qb6

### Ce que l’humain croit
Les Blancs veulent conserver leur fou et acceptent souvent une reprise h qui modifie leur roque.

### Ce que le coup change
Échanger le fou du Londres et provoquer une structure qui offre des cibles.

### Plan simple pour les Noirs
Jouer ...g6, ...Bg7 et ouvrir la colonne h seulement si le roi blanc y roque.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Q protégée, fou exposé : ...Nh5 devient possible.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **5 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B5.2 — LON-07 — Le fou se cache en g5 : ...h6 et ...g5

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. e3 Nc6 5. c3 Qb6 6. Qc2 Nh5 7. Bg5 h6 8. Bh4 g5`  
**Coup-clé :** `g5`  
**Niveau :** Club  
**Famille d’ouverture :** Londres — noyau ...Qb6

### Ce que l’humain croit
Le fou blanc suit un automatisme de conservation et finit par manquer de cases.

### Ce que le coup change
Gagner de l’espace sur l’aile-roi sans mettre son roi en danger, car le centre est contrôlé.

### Plan simple pour les Noirs
Poursuivre par ...g4 si le cavalier f3 est mal placé, sinon consolider avec ...Bg7.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Ne pousse pas les pions pour attaquer le roi : pousse-les pour emprisonner le fou.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B5.3 — TOR-02 — 4.Bh4 : le coup machine ...h5!

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bg5 Ne4 4. Bh4 h5`  
**Coup-clé :** `h5`  
**Niveau :** Club  
**Famille d’ouverture :** Torre

### Ce que l’humain croit
Bh4 applique une règle de conservation du fou mais lui retire ses cases.

### Ce que le coup change
Restreindre le fou et préparer ...f6-g5 sans craindre une attaque de roi immédiate.

### Plan simple pour les Noirs
Après e3, jouer ...f6 ; si Nfd2, échanger ou gagner de l’espace.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Le but de ...h5 n’est pas d’attaquer : c’est de fermer la porte h2.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **11 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B5.4 — TOR-05 — 4.h4 : ignorer l’intimidation

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bg5 Ne4 4. h4 c5`  
**Coup-clé :** `c5`  
**Niveau :** Club  
**Famille d’ouverture :** Torre

### Ce que l’humain croit
h4 cherche à punir ...Nxg5 ou ...f6, mais le roi blanc n’est pas développé.

### Ce que le coup change
Répondre sur le centre plutôt que copier une poussée d’aile.

### Plan simple pour les Noirs
Jouer ...Qb6, ...Nc6 et laisser les Blancs justifier h4.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Contre h4, ne joue pas h5 par réflexe : joue ...c5.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **11 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B5.5 — PST-01 — 2.Bg5 : demander au fou avec ...h6

**Déclencheur :** `1. d4 d5 2. Bg5 h6 3. Bh4 c5`  
**Coup-clé :** `c5`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Veresov et pseudo-Trompowsky

### Ce que l’humain croit
Le pseudo-Trompowsky mise sur un Noir qui développe Nf6 automatiquement.

### Ce que le coup change
Obtenir un tempo utile avant de frapper le centre.

### Plan simple pour les Noirs
Jouer ...cxd4, ...Nc6 et ...Qb6.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Avant de jouer ...Nf6, demande au fou où il veut vivre.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **23 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

# B6 — Règles rigides

## Savoir quand violer un principe classique

**Croyance exploitée :** Il ne faut jamais jouer ...f6, doubler ses pions, fermer par ...c4 ou accepter un gambit.

**Compétence durable :** Une règle est un garde-fou, pas une loi : la géométrie concrète décide.

## B6.1 — ORD-09 — h4 précoce : riposter au centre

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. h4 cxd4 5. Nxd4 Nbd7`  
**Coup-clé :** `Nbd7`  
**Niveau :** Club  
**Famille d’ouverture :** Londres — ordres de coups

### Ce que l’humain croit
h4 cherche à intimider, mais ne développe rien et ne défend pas b2.

### Ce que le coup change
Répondre à une expansion d’aile par une pression centrale immédiate.

### Plan simple pour les Noirs
Ne pas lancer une contre-attaque de pions ; finir le développement et viser d4.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Une attaque d’aile prématurée se punit au centre.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B6.2 — TOR-08 — 4.e3 : le coup concret ...f6

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bg5 Ne4 4. e3 f6`  
**Coup-clé :** `f6`  
**Niveau :** Club  
**Famille d’ouverture :** Torre

### Ce que l’humain croit
e3 consolide d4 mais enferme le fou c1 ; le roi blanc ne peut exploiter la poussée f.

### Ce que le coup change
Chasser le fou et préparer e5 dans un centre fermé.

### Plan simple pour les Noirs
Après Bf4, jouer ...c5 ; après Bh4, g5 peut gagner le fou.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> La poussée ...f6 est saine quand elle gagne un tempo et prépare ...e5.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **11 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B6.3 — TOR-09 — Bh4-h5-f6 : échanger puis enfermer

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bg5 Ne4 4. Bh4 h5 5. e3 f6 6. Nfd2 Nxd2 7. Nxd2 g5`  
**Coup-clé :** `g5`  
**Niveau :** Avancé  
**Famille d’ouverture :** Torre

### Ce que l’humain croit
Les Blancs jouent des coups “sûrs” ; l’échange en d2 retire un défenseur et rend la restriction du fou plus concrète.

### Ce que le coup change
Échanger le cavalier qui pourrait défendre le fou, puis construire une cage de pions.

### Plan simple pour les Noirs
Après ...g5, choisir entre gagner le fou, ouvrir la colonne h ou consolider avec ...e6.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Échange d’abord le bon défenseur, puis compte les cases du fou.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B6.4 — STO-01 — Stonewall : fermer par ...c4!

**Déclencheur :** `1. d4 d5 2. e3 Nf6 3. Bd3 c5 4. f4 c4 5. Be2 Bf5`  
**Coup-clé :** `Bf5`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Stonewall et gambits

### Ce que l’humain croit
Le Stonewall veut Bxh7+ ou e4 ; ...c4 coupe le fou et empêche la rupture facile.

### Ce que le coup change
Fixer le fou d3 hors de sa diagonale d’attaque et gagner de l’espace.

### Plan simple pour les Noirs
Jouer ...e6, ...Nc6 et développer l’aile-dame par ...b5.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Fou d3 + f4 = ferme le centre par ...c4.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **6 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B6.5 — BDG-01 — Blackmar-Diemer : accepter avec ...exf3

**Déclencheur :** `1. d4 d5 2. e4 dxe4 3. Nc3 Nf6 4. f3 exf3 5. Nxf3 Bf5`  
**Coup-clé :** `Bf5`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Stonewall et gambits

### Ce que l’humain croit
Le gambit compte sur un Noir qui défend passivement son pion supplémentaire.

### Ce que le coup change
Accepter le pion puis développer le fou avant ...e6.

### Plan simple pour les Noirs
Développer ...e6, ...Be7 et roquer ; rendre le pion seulement pour simplifier.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Accepte, développe, roque — ne protège pas le pion avec des contorsions.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **10 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

# B7 — Attaque d’aile avant le centre

## Punir les tempos décoratifs

**Croyance exploitée :** Une poussée h ou a crée une attaque, même si mon centre n’est pas stabilisé.

**Compétence durable :** Quand l’adversaire attaque sans avoir fini son centre, répondre au centre est souvent le coup le plus agressif.

## B7.1 — ORD-10 — h3 précoce : prendre l’initiative

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bf4 c5 4. h3 cxd4 5. Nxd4 Qb6`  
**Coup-clé :** `Qb6`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Londres — ordres de coups

### Ce que l’humain croit
h3 est joué par habitude pour offrir h2 au fou.

### Ce que le coup change
Capitaliser sur un tempo prophylactique qui ne répond à aucune menace réelle.

### Plan simple pour les Noirs
Attaquer b2, puis utiliser ...Bf5 ou ...cxd4.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Quand l’adversaire prépare une retraite, avance au centre.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B7.2 — JOB-06 — 4.f3 : ouvrir d4 avant l’attaque

**Déclencheur :** `1. d4 d5 2. Nc3 Nf6 3. Bf4 c5 4. f3 cxd4 5. Qxd4 Nc6`  
**Coup-clé :** `Nc6`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Jobava

### Ce que l’humain croit
f3 affaiblit e3 et le roi tout en plaçant la dame blanche face aux tempos.

### Ce que le coup change
Punir une préparation lente de e4 en ouvrant le centre.

### Plan simple pour les Noirs
Développer ...e5 ou ...Bf5 avec tempo sur la dame.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Quand f3 prépare e4, ouvre le centre avant e4.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B7.3 — JOB-09 — 4.a3 : un tempo décoratif

**Déclencheur :** `1. d4 d5 2. Nc3 Nf6 3. Bf4 c5 4. a3 cxd4 5. Qxd4 Nc6`  
**Coup-clé :** `Nc6`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Jobava

### Ce que l’humain croit
a3 prépare b4 mais ne répond pas à la tension sur d4.

### Ce que le coup change
Ouvrir le centre avant que le coup utile e3 n’arrive.

### Plan simple pour les Noirs
Développer avec tempo et viser e5.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Un coup d’aile sans menace offre un tempo au centre.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B7.4 — JOB-10 — 4.h4 : même sanction centrale

**Déclencheur :** `1. d4 d5 2. Nc3 Nf6 3. Bf4 c5 4. h4 cxd4 5. Qxd4 Nc6`  
**Coup-clé :** `Nc6`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Jobava

### Ce que l’humain croit
h4 cherche une attaque avant que le roi noir ait choisi son aile.

### Ce que le coup change
Montrer que l’agression visuelle n’empêche pas la rupture centrale.

### Plan simple pour les Noirs
Développer ...e5 avec tempo si possible et garder le roi flexible.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Ne réponds pas à h4 par h5 : réponds par le centre.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B7.5 — VER-08 — 4.f3 : ouvrir avant e4

**Déclencheur :** `1. d4 d5 2. Nc3 Nf6 3. Bg5 c5 4. f3 cxd4 5. Qxd4 Nc6`  
**Coup-clé :** `Nc6`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Veresov et pseudo-Trompowsky

### Ce que l’humain croit
f3 affaiblit les diagonales et retarde le cavalier g1.

### Ce que le coup change
Attaquer la dame et le centre avant que f3-e4 ne fonctionne.

### Plan simple pour les Noirs
Développer ...e5 avec tempo et garder le roi flexible.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Comme au Jobava : f3 appelle ...cxd4.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

# B8 — Géométrie tactique machine-humanisée

## Reconnaître les motifs ...d4, ...Qa5+ et ...Ne4

**Croyance exploitée :** Je dois récupérer immédiatement un pion ou répondre directement à une menace locale.

**Compétence durable :** Un tempo sur une pièce, un échec intermédiaire ou un avant-poste central peut être plus urgent que le matériel.

## B8.1 — JOB-03 — 4.dxc5 : la poussée machine ...d4!

**Déclencheur :** `1. d4 d5 2. Nc3 Nf6 3. Bf4 c5 4. dxc5 d4`  
**Coup-clé :** `d4`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Jobava

### Ce que l’humain croit
Les Blancs attendent ...e6 ; ...d4 inverse la question et force une décision.

### Ce que le coup change
Gagner de l’espace et chasser le cavalier au lieu de récupérer immédiatement le pion.

### Plan simple pour les Noirs
Après Nb1, jouer ...e5 ; après Na4, préparer ...Qa5+.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Un pion pris sur l’aile peut être payé par un tempo au centre.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B8.2 — JOB-04 — 4.Nb5 : l’échec qui casse le schéma

**Déclencheur :** `1. d4 d5 2. Nc3 Nf6 3. Bf4 c5 4. Nb5 Qa5+`  
**Coup-clé :** `Qa5+`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Jobava

### Ce que l’humain croit
Le joueur connaît la menace Nc7+ mais oublie que son cavalier c3 ne peut plus bloquer Qa5+.

### Ce que le coup change
Exploiter immédiatement le cavalier éloigné et le roi au centre.

### Plan simple pour les Noirs
Après Nc3, prendre d4 ou jouer ...Na6 selon la tactique.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Nb5 sans c3 disponible appelle ...Qa5+.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B8.3 — JOB-13 — Le double motif : clouage puis ...Qa5+

**Déclencheur :** `1. d4 d5 2. Nc3 Nf6 3. Bf4 c5 4. e3 Bg4 5. Be2 Bxe2 6. Ngxe2 Nc6 7. Nb5 Qa5+`  
**Coup-clé :** `Qa5+`  
**Niveau :** Avancé  
**Famille d’ouverture :** Jobava

### Ce que l’humain croit
Les Blancs retrouvent Nb5, mais leur coordination a changé après l’échange en e2.

### Ce que le coup change
Retirer le défenseur du centre avant d’utiliser l’échec a5.

### Plan simple pour les Noirs
Calculer cxd4 et e5 ; ne pas défendre c7 passivement.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Le motif ...Qa5+ reste vivant tant que Nc3 ne peut interposer.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B8.4 — TOR-06 — 4.Nbd2 : prendre le fou

**Déclencheur :** `1. d4 d5 2. Nf3 Nf6 3. Bg5 Ne4 4. Nbd2 Nxg5 5. Nxg5 e5`  
**Coup-clé :** `e5`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Torre

### Ce que l’humain croit
Nbd2 suppose que le cavalier e4 doit reculer ; il oublie l’échange favorable.

### Ce que le coup change
Échanger la pièce active puis gagner le centre avec tempo.

### Plan simple pour les Noirs
Après ...e5, développer ...Nc6 et viser d4.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Quand le cavalier d2 reprend en g5, le centre e5 devient libre.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

## B8.5 — VER-03 — 4.dxc5 : encore ...d4!

**Déclencheur :** `1. d4 d5 2. Nc3 Nf6 3. Bg5 c5 4. dxc5 d4`  
**Coup-clé :** `d4`  
**Niveau :** Essentiel  
**Famille d’ouverture :** Veresov et pseudo-Trompowsky

### Ce que l’humain croit
Les Blancs prennent sur c5 en s’attendant à ...e6.

### Ce que le coup change
Utiliser le même pattern que contre le Jobava.

### Plan simple pour les Noirs
Chasser le cavalier, jouer ...e5 et récupérer c5 plus tard.

### Si l’adversaire connaît
Le but n’est pas de forcer un piège. Conserver le développement, clarifier le centre lorsque cela améliore les pièces, et revenir au plan structurel indiqué. Une ligne qui ne laisse pas une position normale contre la meilleure défense doit être rétrogradée lors de l’audit V1.

### À retenir
> Nc3 + prise en c5 = vérifie toujours ...d4.

### Preuve disponible
Audit moteur V0.9 : grade **A**, perte maximale enregistrée **0 cp**. Cette mesure est conservée comme héritage et doit être reproduite avec `LAB/scripts/stockfish_audit.py`. Maia‑3, Lichess et relecture externe : **non exécutés dans cette livraison**.

# Parcours par Elo

## 1100–1399 — Reconnaître le déclencheur
Priorité aux ruptures centrales, doubles cibles et motifs tactiques immédiats. Limiter les variantes et verbaliser le plan.

## 1400–1699 — Comprendre la concession
Ajouter structures asymétriques, sorties de dame et réponses aux défenses correctes. Mesurer les erreurs par bande de 200 Elo.

## 1700–1999 — Jouer la position connue des deux camps
La surprise devient secondaire. Le cours doit encore donner une position saine, rare et mieux comprise. Les idées dont l’efficacité s’effondre sont étiquetées “arme de club”, pas “concept durable”.

# Critères de publication

Le cours ne doit pas être présenté comme validé empiriquement avant :

- réexécution de Stockfish 18 sur les 40 lignes ;
- profil Maia‑3 79M aux Elo 1100, 1300, 1500, 1700, 1900 et 2100 ;
- analyse Lichess séparée en découverte, validation et test ;
- revue de la ligne de sécurité par un entraîneur fort ;
- bêta-test en parties rapides ;
- vérification de l’import et des transpositions dans Chessable.
