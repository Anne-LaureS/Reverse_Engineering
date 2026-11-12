# VM Windows « RE-J3 » — préparation et lancement

Le Jour 3 se déroule dans une **VM Windows isolée** (VMware ou VirtualBox,
conforme à la fiche de cours). Cette page liste les outils à embarquer et
comment lancer les cibles. La VM est préparée **une fois** par le formateur et
distribuée aux étudiants avec `kit-etudiant-jour3.zip`.

## Outils à installer dans la VM (tous gratuits)
| Outil | Usage | TP |
|---|---|---|
| **Cheat Engine** | scanner la RAM d'un processus vivant | TP11 |
| **System Informer** (ex-Process Hacker) | processus, régions mémoire, création de dump | TP12, TP13 |
| **HxD** | éditeur hexadécimal, recherche dans un dump | TP12 |
| **x64dbg** (inclut x32dbg) | débogueur graphique, *Attach*, pile/registres | TP13, TP14 |
| **Ghidra 12.2** | décompilateur (lecture des fonctions, adresse de `win`) | TP11–TP14 |
| **Python 3** | scripts à trou `recompose.py`, `payload.py` | TP12, TP14 |
| **Strings** (Sysinternals) | montrer qu'un secret est absent du disque | TP11, TP12 |

> Ghidra nécessite un **JDK 21+** dans la VM. Python doit être accessible en
> ligne de commande (`python`).

## Réglages de la VM
- **Pas de réseau sortant** : toutes les cibles sont locales et inertes.
- Lancer **Cheat Engine** et **x64dbg** en **administrateur** (clic droit →
  *Exécuter en tant qu'administrateur*) : sans cela, l'accès à la mémoire d'un
  autre processus échoue.
- Ne pas modifier les cibles du TP14 : elles sont compilées en 32 bits, sans
  protections, pour que l'adresse de `win()` soit fixe.

## Déposer le kit et lancer les cibles
1. Copier `kit-etudiant-jour3.zip` dans la VM, le décompresser (par exemple dans
   `C:\RE-J3\`).
2. Chaque TP est un dossier : `tp11`, `tp12`, `tp13`, `tp14`. La cible de
   **démonstration** est à la racine du dossier ; la cible de **groupe** est
   dans le sous-dossier `tp\`.
3. Lancer une cible en **double-cliquant** le `.exe`, ou depuis un invite de
   commandes :
   ```bat
   cd C:\RE-J3\tp11
   gestionnaire.exe
   ```
4. Pour le TP14, la charge utile se donne par **redirection d'un fichier**, pas
   au clavier :
   ```bat
   cd C:\RE-J3\tp14
   python ..\tp14\tp\payload.py > payload.bin
   type payload.bin | acces.exe
   ```

## En cas de souci
- *Cheat Engine ne voit pas le processus* : l'avoir lancé en administrateur, et
  garder la fenêtre de la cible ouverte.
- *Le point d'arrêt x64dbg ne tombe pas* : avoir bien fait *Attach* (et non
  rouvrir le `.exe`), puis saisir une valeur dans la fenêtre de la cible.
- *Le TP14 ne détourne pas vers `win`* : vérifier le décalage (motif cyclique)
  et l'adresse de `win` relue dans Ghidra ; l'entrée doit venir d'un fichier.
- *Un plantage s'affiche après le drapeau du TP14* : c'est normal (voir
  CONSIGNES).
