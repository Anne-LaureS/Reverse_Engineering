# VM Windows « RE-J3 » — Jour 4 (ajouts et lancement)

Le Jour 4 réutilise la **même VM Windows** que le Jour 3. Cette page liste les
ajouts et comment lancer les cibles. La VM est préparée par le formateur et
distribuée avec `kit-etudiant-jour4.zip`.

> **Monter la VM** : voir `reverse3/vm-kvm.md` (QEMU/KVM + virt-manager).

## Outils (en plus de ceux du Jour 3)
| Outil | Usage | TP |
|---|---|---|
| **x32dbg** (suite x64dbg) | débogueur **32 bits** (cibles du TP15) | TP15 |
| **x64dbg** (déjà présent) | débogueur **64 bits** ; patch des vérifications | TP16 |
| **ScyllaHide** (greffon x64dbg) | masquer l'anti-debug automatiquement | TP16 |
| **Ghidra** (déjà présent) | lire le code des cibles | TP15, TP16, TP18 |
| **PE-bear** ou **CFF Explorer** (option) | lire ASLR/DEP en GUI | TP15, TP18 |
| **Python 3** (déjà présent) | `serve.py`, `defense.py`, `lire_protections.py` | TP15, TP17 |
| **Navigateur + DevTools** | TP web (CSP, requêtes forgées) | TP17 |

> **Aucun compilateur n'est nécessaire dans la VM** : toutes les cibles sont
> fournies compilées. Le TP18 se fait en complétant un source et en comparant
> les binaires fournis.

## Réglages
- Lancer **x32dbg** (TP15, cibles 32 bits) ou **x64dbg** (TP16, cibles 64 bits)
  en administrateur.
- TP17 : `serve.py` écoute sur **127.0.0.1** uniquement ; pas de réseau sortant.

## Déposer le kit et lancer les cibles
1. Décompresser `kit-etudiant-jour4.zip` (par exemple dans `C:\RE-J4\`).
2. **TP15** — protections mémoire (cibles **32 bits** → x32dbg) :
   ```bat
   cd C:\RE-J4\tp15
   python tp\lire_protections.py sans-protection.exe
   REM Fabriquer payload.bin (ret2win, offset 76) avec les outils fournis :
   REM   dans ..\outils\payload.py, mettre OFFSET=76 et WIN_ADDR=0x00401648
   python ..\outils\payload.py > payload.bin
   type payload.bin | sans-protection.exe      REM ret2win : drapeau affiché
   type payload.bin | canari.exe               REM canari : bloqué (pas de drapeau)
   ```
3. **TP16** — anti-debug : ouvrir `tp16\protege.exe` **dans** x64dbg (ou s'y
   attacher) pour voir le blocage, puis neutraliser les vérifications.
4. **TP17** — web :
   ```bat
   cd C:\RE-J4
   python serve.py
   ```
   puis ouvrir http://127.0.0.1:8000/tp17/ ; compléter `defense.py` et relancer.
5. **TP18** — code sécurisé (**pas de compilation** : on complète le source et
   on compare les binaires **fournis**). Compléter `tp18\tp\securise.c`, puis
   fabriquer la charge ret2win **offset 108** (dans `..\outils\payload.py` :
   `OFFSET=108`, `WIN_ADDR=0x00401648` — ce programme a un champ en plus que le
   TP15, d'où 108 et non 76) et l'envoyer aux deux binaires :
   ```bat
   cd C:\RE-J4
   python outils\payload.py > tp18\payload.bin
   type tp18\payload.bin | tp18\vulnerable.exe   REM drapeau (faille)
   type tp18\payload.bin | tp18\securise.exe     REM pas de drapeau (durci)
   ```

## En cas de souci
- *Le TP15 n'affiche pas d'ASLR aléatoire* : normal hors VM réelle ; le **bit**
  PE se lit toujours, la randomisation d'adresses se montre dans la VM Windows.
- *Le TP16 affiche le drapeau sans rien faire* : c'est qu'aucun débogueur n'est
  attaché ; le défi est de l'obtenir **sous** débogueur.
- *Le TP17 : la CSP ne bloque pas l'inline* : vérifier l'en-tête dans l'onglet
  Network, et recharger après avoir relancé `serve.py`.
