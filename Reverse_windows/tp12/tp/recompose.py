#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP12 - groupe : recomposition d'un secret masque trouve dans un dump memoire.

Tout est deja ecrit SAUF deux valeurs a completer (les TODO). Vous n'avez pas
a programmer : il faut lire le dump dans HxD, reperer le marqueur VAULTBEG,
observer les octets masques du champ 'secret', puis remplir les deux trous.

Usage :
    python recompose.py chemin_du_dump.dmp
"""
import sys

# --- A COMPLETER -----------------------------------------------------------
# TODO(1): octet de XOR a appliquer pour demasquer le secret (format 0xNN).
#          Indice : testez les valeurs jusqu'a obtenir du texte lisible, ou
#          deduisez-le d'un octet connu (ex. un tiret '-' = 0x2D).
XOR_KEY = 0x00           # <<< remplacez 0x00 par la bonne octet-cle

# TODO(2): longueur du champ 'secret' a lire apres le marqueur (en octets).
#          Indice : le secret se termine avant le marqueur VAULTEND.
SECRET_LEN = 0           # <<< remplacez 0 par la bonne longueur
# ---------------------------------------------------------------------------

BEG = b"VAULTBEG"
# Disposition de la structure en memoire (cf. CONSIGNES) :
#   beg[8] | user[16] | secret[32] | end[8]
# Le champ 'secret' commence donc 8 + 16 = 24 octets apres le debut de BEG.
SECRET_OFFSET_FROM_BEG = 8 + 16


def main():
    if len(sys.argv) != 2:
        print("Usage : python recompose.py chemin_du_dump.dmp")
        return 1
    with open(sys.argv[1], "rb") as f:
        data = f.read()

    pos = data.find(BEG)
    if pos < 0:
        print("Marqueur VAULTBEG introuvable dans le dump.")
        return 1

    start = pos + SECRET_OFFSET_FROM_BEG
    masked = data[start:start + SECRET_LEN]
    clear = bytes(b ^ XOR_KEY for b in masked)
    print("Octets masques :", masked.hex(" "))
    print("Secret recompose :", clear.decode("latin-1"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
