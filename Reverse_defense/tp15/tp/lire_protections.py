#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP15 - lire les protections d'un executable Windows (PE).

Le champ DllCharacteristics de l'en-tete PE indique quelles protections sont
demandees au chargeur. Pas besoin de coder : il faut completer les deux masques
de bits (les TODO), puis lancer le script sur chaque .exe pour comparer.

Usage :
    python lire_protections.py cible.exe
"""
import struct
import sys

# --- A COMPLETER -----------------------------------------------------------
# Bits du champ DllCharacteristics (doc officielle du format PE) :
# TODO(1): masque de l'ASLR (DYNAMIC_BASE).  Indice : 0x00??
ASLR_BIT = 0x0040       # <<< remplacez par le bon masque (ASLR / DYNAMIC_BASE)

# TODO(2): masque du DEP (NX_COMPAT).        Indice : 0x0???
DEP_BIT = 0x0100        # <<< remplacez par le bon masque (DEP / NX_COMPAT)
# ---------------------------------------------------------------------------

HIGH_ENTROPY_BIT = 0x0020
CFG_BIT = 0x4000


def dll_characteristics(path):
    with open(path, "rb") as f:
        data = f.read()
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]       # offset en-tete PE
    # En-tete optionnel = e_lfanew + 4 (signature) + 20 (COFF) = e_lfanew + 24.
    # DllCharacteristics est a l'offset 0x46 de l'en-tete optionnel.
    return struct.unpack_from("<H", data, e_lfanew + 24 + 0x46)[0]


def main():
    if len(sys.argv) != 2:
        print("Usage : python lire_protections.py cible.exe")
        return 1
    dc = dll_characteristics(sys.argv[1])
    print("DllCharacteristics = 0x%04X" % dc)
    print("  ASLR (DYNAMIC_BASE) :", "oui" if dc & ASLR_BIT else "non")
    print("  DEP  (NX_COMPAT)    :", "oui" if dc & DEP_BIT else "non")
    print("  High-entropy ASLR   :", "oui" if dc & HIGH_ENTROPY_BIT else "non")
    print("  Control Flow Guard  :", "oui" if dc & CFG_BIT else "non")
    print("(Le canari de pile n'est pas un bit PE : il se voit a l'execution,")
    print(" via l'arret brutal du programme lors du debordement, avant win().)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
