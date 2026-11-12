#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP09 - travail de groupe (/tp09/tp/) : decodeur de la charge exfiltree.

Schema trouve par analyse statique (analytics.js deobfusque, fonctions
_0x1d29fa / _0x1fd993) :
    1. payload = {"t": <epoch ms>, "page": <chemin>, "data": {name, card, exp, cvv}}
    2. texte = JSON.stringify(payload)
    3. chaque caractere du texte est XOR avec la constante 66 (0x42)
    4. le resultat est encode en base64 (btoa)

Ce script fait l'inverse : base64 puis XOR 66, pour relire une ligne de
collector.log en clair. Il sert aussi a fabriquer une charge de test, pour
verifier que le serveur accepte bien ce format (round-trip).
"""

import base64
import json
import sys

XOR_KEY = 66  # 0x42, constante _0x4a5c6c relevee dans analytics.js


def encode(obj: dict) -> str:
    text = json.dumps(obj, separators=(",", ":"))
    xored = bytes((ord(c) ^ XOR_KEY) & 0xFF for c in text)
    return base64.b64encode(xored).decode()


def decode(b64_text: str) -> dict:
    xored = base64.b64decode(b64_text)
    text = bytes((b ^ XOR_KEY) & 0xFF for b in xored).decode("utf-8")
    return json.loads(text)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--last-log":
        log_path = sys.argv[2] if len(sys.argv) > 2 else "../../collector.log"
        with open(log_path, encoding="utf-8") as f:
            line = f.read().strip().splitlines()[-1]
        # format : "AAAA-MM-JJ HH:MM:SS <base64>"
        b64 = line.split(" ", 2)[2]
        print(json.dumps(decode(b64), indent=2, ensure_ascii=False))
    elif len(sys.argv) > 1:
        print(json.dumps(decode(sys.argv[1]), indent=2, ensure_ascii=False))
    else:
        print(__doc__)
