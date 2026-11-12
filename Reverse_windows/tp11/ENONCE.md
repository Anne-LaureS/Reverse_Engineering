# TP11 — Extraction d'un secret en mémoire vive

## Objectif
Un logiciel détient une **clé de session** en clair, mais uniquement **en
mémoire**, le temps qu'il tourne : elle n'est jamais écrite en clair sur le
disque. Vous allez la lire **dans la RAM du processus** avec Cheat Engine, sans
toucher au code.

## Mise en route
Dans la VM Windows, double-cliquez sur `tp11\tp\gestionnaire.exe`. **Laissez la
fenêtre ouverte** : le secret disparaît dès que le programme se ferme.

## Outils
- **Cheat Engine** (scanner de mémoire, à lancer en administrateur).
- `strings` (ou l'outil Strings de Sysinternals) pour vérifier que le secret
  est absent du fichier.

## À vous de jouer
La cible contient une clé que vous ne connaissez pas. Votre propre saisie est
votre point de repère.
1. Lancez la cible, saisissez un **nom repérable** (long et rare).
2. Dans Cheat Engine : *File → Open Process* → choisissez la cible.
3. Scannez votre nom (*Value Type* = **String**, *First Scan*).
4. Ouvrez la région trouvée (*Browse this memory region*) et **lisez la clé**
   rangée à quelques octets de là.
5. Vérifiez avec `strings` que la clé n'apparaît **pas** dans le fichier `.exe`.

## Livrable
- Une capture du *Memory Viewer* montrant la clé.
- L'adresse de la clé.
- Une phrase expliquant pourquoi `strings` sur le fichier ne la révèle pas.

## Bonus
- Avec *Next Scan* + *Unknown initial value*, retrouvez une valeur que vous ne
  connaissez pas d'avance.
- Modifiez la clé **en mémoire** depuis Cheat Engine et observez : la mémoire
  d'un processus est aussi **modifiable**, pas seulement lisible.

## Restitution
Puisque tout secret finit en clair dans la RAM, qu'est-ce qui protège vraiment
une clé — et que peut-on seulement ralentir ?
