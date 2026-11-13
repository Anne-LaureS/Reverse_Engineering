# TP18 — Écrire du code source sécurisé

## Objectif
Corriger, à la source, le programme vulnérable des jours précédents — deux
changements ciblés — et vérifier que l'exploit du Jour 3 **ne marche plus**. Pas
de réécriture : vous complétez deux trous.

## Mise en route
Deux binaires sont fournis dans `tp18\` :
- `vulnerable.exe` : le programme fautif ;
- `securise.exe` : la version corrigée (fournie, pour vérifier votre
  raisonnement).

Le fichier à compléter est `tp\securise.c`. Vous ne compilez pas : vous comparez
le comportement des deux binaires. Vous aurez besoin d'une **charge ret2win pour
`vulnerable.exe`** : fabriquez-la avec le dossier `outils\` (`motif.py` +
`payload.py`, voir `outils\README.md`). **Attention** : ce programme a un champ
`secret` en plus — son décalage **n'est pas** celui du Jour 3. Remesurez-le avec
`motif.py` (vous trouverez **108**), puis mettez `OFFSET = 108` et l'adresse de
`win()` dans `payload.py`.

## Outils
- Le dossier `outils\` (`motif.py` + `payload.py`) pour fabriquer la charge
  ret2win adaptée à `vulnerable.exe` (décalage **108**).
- Un éditeur de texte pour compléter `securise.c`.
- **Ghidra** pour comparer la lecture d'entrée dans les deux binaires.

## À vous de jouer
1. Complétez les **deux TODO** de `securise.c` :
   - lecture **bornée** (remplacer `scanf("%s", buf)` par un `fgets` limité à la
     taille du tampon) ;
   - **effacement** du secret avant la fin de la fonction (`memset`).
2. Vérifiez votre raisonnement : envoyez **la même charge** (offset 108) à
   `vulnerable.exe` (drapeau obtenu) puis à `securise.exe` (**pas** de drapeau).
3. Pour **chaque** correction, dites quelle attaque des jours précédents elle
   neutralise (TP14/TP15 pour le débordement ; TP11–TP13 pour le secret).

## Livrable
- Le `securise.c` complété.
- Le tableau « correction → attaque neutralisée ».

## Bonus
- Ajoutez une **validation de longueur** explicite et un message d'erreur propre
  si l'entrée est trop longue. Dites pourquoi « échouer proprement » fait partie
  du code sécurisé.

## Restitution
Des protections (TP15) ou un code correct (TP18), que choisiriez-vous si vous ne
pouviez en avoir qu'un seul — et pourquoi la bonne réponse est « les deux » ?
