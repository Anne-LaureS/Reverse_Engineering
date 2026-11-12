# TP13 — Débogueur sur un processus actif

## Objectif
S'attacher à un programme **déjà lancé**, le mettre en **pause** au moment où il
vérifie un mot de passe, et soit **lire** le secret, soit **forcer** la
vérification. Ici, pas de `strcmp` simple : le mot de passe n'apparaît pas en
clair dans un registre.

## Mise en route
Lancez `tp13\tp\portail.exe`. Le programme tourne en boucle et demande un mot de
passe. **Laissez-le tourner** et attachez-vous à lui.

## Outils
- **x64dbg** (cible 64 bits), lancé en administrateur.
- **Ghidra** pour repérer, à froid, la fonction de vérification (`check`).

## À vous de jouer
Chaque caractère saisi est transformé (XOR à clé glissante) puis comparé à une
table ; aucun registre ne contient le mot de passe en clair.
1. Attachez x64dbg au processus (*File → Attach*) et retrouvez `check`.
2. Au choix :
   - **Contourner** : posez un point d'arrêt sur la branche d'échec et forcez la
     réussite (drapeau `ZF`, ou `jne`→`je`) — vous entrez sans connaître le mot
     de passe ;
   - **Inverser** : lisez en mémoire la table de comparaison et la clé de
     transformation, puis recalculez le mot de passe attendu.
3. Obtenez « Acces autorise ».

## Livrable
- Une capture de l'accès autorisé.
- La méthode choisie (patch ou inversion) ; si inversion, le mot de passe
  retrouvé.

## Bonus
- Faites **les deux** : contournez d'abord (rapide), puis retrouvez vraiment le
  mot de passe (preuve). Expliquez pourquoi l'inversion est une meilleure preuve
  d'analyse.

## Restitution
Attaché à un processus, on peut tout lire et tout modifier ; que reste-t-il
alors comme protection réelle ?
