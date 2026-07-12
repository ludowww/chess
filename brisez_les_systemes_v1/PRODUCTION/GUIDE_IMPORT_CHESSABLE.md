# Guide d’import Chessable V1

1. Créer un cours privé avec huit chapitres correspondant aux fichiers `01` à `08`.
2. Importer d’abord `00_parcours_essentiel_20.pgn` dans une section de démarrage rapide distincte.
3. Entraîner le côté **Noir**.
4. Importer ensuite un PGN par biais humain, sans inclure le fichier `90_bibliotheque...`.
5. Utiliser `99_cours_v1_core_40.pgn` uniquement pour contrôle global ou sauvegarde.
6. Vérifier les transpositions : une même position ne doit pas produire deux obligations contradictoires.
7. Autoriser les alternatives seulement lorsqu’elles servent le même plan et ont passé l’audit moteur.
8. Tester la charge de répétition avec un compte bêta : le parcours essentiel doit rester nettement plus léger que le cours complet.
9. Contrôler les commentaires sur mobile ; raccourcir les répétitions, jamais la phrase mémoire ou la ligne de sécurité.
10. Ne publier qu’après la checklist `CHECKLIST_PUBLICATION.md`.
