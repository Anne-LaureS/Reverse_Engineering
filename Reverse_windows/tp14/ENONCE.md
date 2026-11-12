# TP14 — Buffer Overflow : détourner l'exécution (ret2win)

## Objectif
Un programme lit une entrée dans un tampon de pile trop court. En débordant ce
tampon, vous allez écraser l'**adresse de retour** pour faire sauter le
programme dans une fonction `win()` qui n'est jamais appelée (un « ret2win »).
On s'arrête là : pas de shellcode.

## Mise en route
La cible est en **32 bits**, sans protections. Lancez `tp14\tp\acces.exe`.
L'entrée se donnera par **redirection d'un fichier**, pas au clavier.

## Outils
- **Ghidra** : lire la fonction vulnérable et **l'adresse de `win()`**.
- **x32dbg** : voir l'adresse de retour s'écraser, trouver le décalage.
- **Python** : `payload.py` (script **à compléter**) fabrique la charge utile.

## À vous de jouer
La taille du tampon et le drapeau diffèrent de la démonstration.
1. Dans Ghidra, relevez l'**adresse de `win()`** sur la cible de groupe.
2. Dans x32dbg, envoyez un **motif cyclique** (`Aa0Aa1Aa2…`) et lisez EIP pour
   déduire le **décalage** exact.
3. Complétez les **deux trous** de `payload.py` (le décalage, l'adresse de
   `win()`), puis générez : `python payload.py > payload.bin`.
4. Déclenchez : `type payload.bin | acces.exe`, et récupérez le **drapeau**
   `TP14-TP{...}`.

> Un plantage **après** l'affichage du drapeau est normal : `win()` ne revient
> pas proprement ; le drapeau, lui, est déjà obtenu.

## Livrable
- Le décalage trouvé.
- L'adresse de `win()`.
- Le drapeau obtenu.

## Bonus
- Expliquez, schéma de pile à l'appui, **pourquoi** le décalage n'est pas
  exactement la taille du tampon.
- Dites laquelle des trois protections du Jour 4 (canari, ASLR, DEP) suffirait,
  à elle seule, à empêcher **ce** ret2win.

## Restitution
On a détourné l'exécution sans injecter de code ; qu'est-ce que cela dit de la
frontière entre « données » et « adresses » sur la pile ?
