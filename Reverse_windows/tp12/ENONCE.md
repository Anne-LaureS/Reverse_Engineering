# TP12 — Dump et analyse de la mémoire d'un processus

## Objectif
Prendre un **instantané** (un *dump*) de la mémoire d'un processus, puis y
retrouver un secret hors ligne — comme un analyste qui reçoit l'image mémoire
d'une machine. Ici, le secret reste **masqué** dans le dump : vous devrez le
recomposer.

## Mise en route
Lancez `tp12\tp\coffre.exe` et laissez la fenêtre ouverte pendant la capture.

## Outils
- **System Informer** (ex-Process Hacker) : créer un dump.
- **HxD** : éditeur hexadécimal, recherche dans le dump.
- `recompose.py` (script **à compléter**, dans `tp12\tp\`).

## À vous de jouer
1. Capturez la mémoire du processus (System Informer → clic droit →
   *Create dump file*).
2. Ouvrez le dump dans **HxD** et repérez le marqueur `VAULTBEG`.
3. Relevez les octets du champ secret (il suit le marqueur et l'identifiant ;
   il reste **masqué**, donc illisible tel quel).
4. Complétez les **deux trous** de `recompose.py` (l'octet de XOR à appliquer,
   la longueur du secret), puis lancez-le : `python recompose.py coffre.dmp`.
5. Lisez la clé recomposée.

## Livrable
- L'octet de XOR trouvé et la longueur du secret.
- La clé recomposée.
- Une capture HxD de la zone masquée.

## Bonus
- Retrouvez l'octet de XOR **sans tâtonner** : un octet connu du clair (par
  exemple un tiret `-`, `0x2D`) comparé à l'octet masqué donne la clé. Expliquez
  la méthode.

## Restitution
Entre « lisible dans le dump » et « masqué dans le dump », qu'est-ce que ça
change pour l'analyste — et qu'est-ce que ça ne change pas ?
