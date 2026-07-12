# Restauration du paquet Human Chess Lab V1

Le projet complet **Brisez les systèmes — Human Chess Lab V1.0 RC1** est stocké dans `bootstrap/archive/` sous forme d’une archive `tar.xz` encodée en Base64 et divisée en 20 segments.

Cette représentation textuelle permet de transporter le paquet de façon fiable via le connecteur GitHub. Les scripts de restauration refusent toute archive incomplète ou corrompue.

## Linux et macOS

```bash
bash bootstrap/restore_bundle.sh
```

## Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File bootstrap/restore_bundle.ps1
```

## Vérifications effectuées par les scripts

1. présence exacte des segments `part00` à `part19` ;
2. décodage Base64 strict ;
3. contrôle SHA-256 :

```text
c88f59116ffd8eddd5c0254508b814e7f84d2efdef9ff6ccce0dc62729aec225
```

4. extraction de l’archive ;
5. présence de `brisez_les_systemes_v1/LAB/README_LAB.md`.

## Après restauration

```bash
cd brisez_les_systemes_v1
chmod +x LAB/run_static_qa.sh
./LAB/run_static_qa.sh
```

Le paquet contient notamment :

- le manuscrit français V1 ;
- les PGN du parcours essentiel et des 40 idées centrales ;
- les cartes mémoire ;
- le manifeste et les scorecards ;
- les scripts Stockfish, Maia-3 et Lichess ;
- les tests statiques ;
- les audits historiques clairement identifiés comme non reproduits dans la RC1.

## Workflow recommandé pour Hermes

Après restauration, Hermes doit créer une branche séparée, par exemple :

```bash
git switch -c work/empirical-validation-v1
```

Il peut ensuite suivre `brisez_les_systemes_v1/LAB/README_LAB.md` pour exécuter Stockfish 18, Maia-3 et la validation Lichess. Les résultats empiriques ne doivent pas être ajoutés directement à la branche de bootstrap.
