#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP10 - travail de groupe (/tp10/tp/) : solveur de la cle de licence.

Analyse statique (wasm2wat / module texte) de tp10/tp/license.wasm, et
lecture de tp10/tp/app.js pour la valeur fournie par l'import "env.seed".

Structure de check(len) (fonction exportee), une fois les offsets relatifs
remis a plat (base memoire : table de donnees a 0x10000, zone d'entree
("buffer") a 0x10020, soit +32 par rapport a la table) :

    si len != 17 : invalide
    seed = env.seed()                      -- fourni par le JS, ici :
                                               XOR de "licence" avec 29
    si (seed ^ cle[0]) != 0x30 (48) : invalide
    pour k = 1 .. 16 :
        table[k] == cle[k] ^ (k + 19) ^ seed     -- doit etre vrai pour les 17 octets

Comme XOR est sa propre inverse :
    cle[0] = seed ^ 0x30
    cle[k] = table[k] ^ (k + 19) ^ seed            pour k = 1..16

Table (17 octets, segment Data du module, releve avec le module texte) :
    35 16 83 14 21 95 92 30 94 53 33 59 54 1 99 7 24
"""

TABLE = [35, 16, 83, 14, 21, 95, 92, 30, 94, 53, 33, 59, 54, 1, 99, 7, 24]


def compute_seed() -> int:
    """Reproduit imports.env.seed() de tp10/tp/app.js."""
    seed = 29
    for ch in "licence":
        seed ^= ord(ch)
    return seed


def solve() -> str:
    seed = compute_seed()
    key = [0] * len(TABLE)
    key[0] = seed ^ 0x30
    for k in range(1, len(TABLE)):
        key[k] = TABLE[k] ^ (k + 19) ^ seed
    return bytes(key).decode("ascii")


if __name__ == "__main__":
    seed = compute_seed()
    key = solve()
    print(f"seed (env.seed())  : {seed}")
    print(f"longueur attendue  : {len(key)}")
    print(f"cle de licence     : {key}")
