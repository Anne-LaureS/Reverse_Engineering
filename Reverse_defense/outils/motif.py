#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outil du Jour 4 - motif cyclique (mesure du decalage).

Sert a (re)trouver le decalage de la charge utile ret2win du Jour 3, utile
pour le TP15 (la rejouer contre `durci.exe`) et le TP18 (la rejouer contre
`vulnerable.exe`). Aucun code a ecrire, deux usages :

  1) Generer un motif NON repetitif a envoyer a la cible :
         python motif.py gen 200 > motif.bin
         puis, cote Windows :   type motif.bin | vulnerable.exe
     La cible plante en sautant dans une valeur tiree du motif.

  2) Retrouver le decalage a partir de la valeur qui a ecrase EIP dans x32dbg
     (le registre EIP affiche par exemple 63413563) :
         python motif.py find 0x63413563
     -> affiche le nombre d'octets de remplissage avant l'adresse de retour.
        C'est ce nombre qu'on recopie dans OFFSET de payload.py.

Le motif est le meme que celui de Metasploit (pattern_create) : des blocs de
3 caracteres majuscule/minuscule/chiffre (Aa0 Aa1 Aa2 ...), uniques sur plus de
20000 octets, donc 4 octets suffisent a situer la position sans ambiguite.
Il ne contient ni espace ni retour a la ligne : scanf("%s") le lit en entier.
"""
import struct
import sys

UPPER = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = b"abcdefghijklmnopqrstuvwxyz"
DIGITS = b"0123456789"


def pattern(length):
    """Renvoie les `length` premiers octets du motif cyclique."""
    out = bytearray()
    for u in UPPER:
        for l in LOWER:
            for d in DIGITS:
                if len(out) >= length:
                    return bytes(out[:length])
                out += bytes((u, l, d))
    return bytes(out[:length])  # periode max : 26*26*10*3 = 20280 octets


def needle_from(token):
    """Transforme l'argument de `find` en 4 octets a chercher dans le motif.

    - une valeur hex d'EIP (0x63413563 ou 63413563) -> octets petit-boutiste,
      exactement comme ils etaient en memoire ;
    - sinon, une courte chaine ASCII (ex. c5Ac) prise telle quelle.
    """
    t = token.lower()
    if t.startswith("0x"):
        t = t[2:]
    if len(t) == 8 and all(c in "0123456789abcdef" for c in t):
        return struct.pack("<I", int(t, 16))
    return token.encode("latin-1")


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "gen":
        length = int(sys.argv[2]) if len(sys.argv) >= 3 else 200
        sys.stdout.buffer.write(pattern(length))
        return
    if len(sys.argv) >= 3 and sys.argv[1] == "find":
        needle = needle_from(sys.argv[2])
        idx = pattern(20280).find(needle)
        if idx < 0:
            sys.stderr.write("Valeur introuvable dans le motif : %r\n" % needle)
            sys.exit(1)
        print(idx)
        return
    sys.stderr.write(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
