# TP15 — Protections de la mémoire en action

## Objectif
Reprendre le programme vulnérable du Jour 3 (le ret2win) et voir comment les
protections modernes (canari, ASLR, DEP) l'arrêtent. Vous ne codez pas : vous
comparez des binaires et lisez leurs protections.

## Mise en route
Les binaires sont fournis dans `tp15\`. La cible de groupe `tp\durci.exe` cumule
**toutes** les protections. Vous aurez besoin de la **charge utile du Jour 3**
(76 octets + adresse de `win()`), dans un fichier `payload.bin`. Pas besoin de
l'avoir gardée : les scripts du dossier `outils\` (`motif.py` + `payload.py`)
permettent de la **refabriquer** (voir `outils\README.md`).

## Outils
- **x32dbg** : voir le débordement et le canari.
- `lire_protections.py` (script **à compléter**) ou **PE-bear / CFF Explorer**
  pour lire les protections d'un `.exe`.

## À vous de jouer
1. Complétez les **deux masques** de `lire_protections.py` (ASLR, DEP) et lisez
   les protections de `tp\durci.exe`.
2. Tentez la charge utile du Jour 3 contre `durci.exe` : constatez l'échec.
3. **Expliquez**, protection par protection, pourquoi le ret2win ne marche plus
   (canari ? adresse non fixe ? les deux ?).

## Livrable
- Le tableau des protections de `durci.exe` (ASLR, DEP).
- Le résultat de l'attaque.
- L'explication de ce qui l'a bloquée.

## Bonus
- Dites laquelle, **à elle seule**, suffirait à bloquer ce ret2win (indice :
  celle qui porte sur l'adresse de retour ou sur la prévisibilité de `win()`).

## Restitution
Aucune protection ne « répare » le code ; chacune ferme une porte. Laquelle
manque encore, et que reste-t-il à corriger dans le source lui-même ?
