# Outils — refabriquer la charge utile ret2win du Jour 3

Le TP15 et le TP18 vous demandent une **charge ret2win** (`payload.bin` :
remplissage jusqu'à l'adresse de retour + adresse de `win()`). Ces deux scripts
permettent de la **refaire facilement**, sans rien réinstaller du Jour 3.

> ⚠️ **Le décalage dépend de la cible** : il vaut **76** pour les binaires du
> TP15 (même code que le Jour 3) mais **108** pour `vulnerable.exe` du TP18 (ce
> programme a un champ `secret` en plus). **Remesurez-le** à chaque fois avec
> `motif.py` plutôt que de le supposer.

## `motif.py` — générer une séquence et mesurer le décalage
Motif cyclique non répétitif (identique à `pattern_create` de Metasploit).

```bash
# 1) générer un motif et l'envoyer à la cible
python motif.py gen 200 > motif.bin
#    côté Windows :   type motif.bin | vulnerable.exe

# 2) lire EIP dans x32dbg (ex. 63413563) et retrouver le décalage
python motif.py find 0x63413563
#    -> affiche le nombre d'octets de remplissage (OFFSET)
```

## `payload.py` — assembler la charge utile
Deux valeurs à compléter (les `TODO`), puis :

```bash
python payload.py > payload.bin
#    côté Windows :   type payload.bin | vulnerable.exe
```

- `OFFSET` : le décalage rendu par `motif.py find`.
- `WIN_ADDR` : l'adresse de `win()` lue dans Ghidra (ex. `0x00401648`).

> Le décalage et l'adresse peuvent différer d'un binaire à l'autre
> (`vulnerable.exe`, `durci.exe`…) : remesurez-les sur la cible visée.
