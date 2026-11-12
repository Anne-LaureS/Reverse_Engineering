#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serveur de laboratoire — Jour 2 (analyse d'applications web).

Stdlib uniquement, ecoute UNIQUEMENT sur 127.0.0.1.

Usage (depuis le dossier distribue, ou depuis la racine formateur) :
    python3 serve.py              # tous les TP
    python3 serve.py tp08         # un seul TP (les autres renvoient 404)
    python3 serve.py --port 8001

Ce fichier ne contient aucune donnee propre aux TP. Les routes et les reponses
sont dans _lab.json (genere par build.py) : chemins indexes par empreinte
SHA-256, chaines masquees. Lire ce serveur ne donne donc ni les endpoints
caches ni les cles. Un etudiant determine peut demasquer _lab.json : la
consigne est de travailler depuis le navigateur.

Tout est local et simule : aucune donnee reelle, aucune communication externe.
"""

import base64
import hashlib
import hmac
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
# Kit etudiant : serve.py est a cote des dossiers tpXX. Racine formateur :
# les artefacts sont dans distrib/.
ROOT = HERE if os.path.isdir(os.path.join(HERE, "tp07")) else os.path.join(HERE, "distrib")
LAB_FILE = os.path.join(ROOT, "_lab.json")
COLLECTOR_LOG = os.path.join(HERE, "collector.log")
MASK = 0xA5

CTYPES = {
    ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
    ".map": "application/json; charset=utf-8", ".wasm": "application/wasm",
    ".md": "text/plain; charset=utf-8", ".txt": "text/plain; charset=utf-8",
    ".svg": "image/svg+xml", ".png": "image/png",
}


def unmask(s):
    return bytes(b ^ MASK for b in base64.b64decode(s)).decode("utf-8")


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_routes():
    if not os.path.isfile(LAB_FILE):
        sys.exit("_lab.json introuvable dans %s : lancer build_all.sh (formateur)." % ROOT)
    with open(LAB_FILE, encoding="utf-8") as f:
        return json.load(f)["routes"]


ROUTES = load_routes()
ONLY = None  # "tp08" pour ne servir qu'un TP


class Handler(BaseHTTPRequestHandler):
    server_version = "LabJ2/2.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False))

    def _allowed(self, path):
        if ONLY is None:
            return True
        return path.startswith("/%s/" % ONLY) or path.startswith("/api/%s/" % ONLY) \
            or path in ("/", "/%s" % ONLY)

    def do_GET(self):
        self._dispatch(b"")

    def do_HEAD(self):
        self._dispatch(b"")

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        self._dispatch(self.rfile.read(n) if n else b"")

    def _dispatch(self, body):
        path = urlparse(self.path).path
        if not self._allowed(path):
            return self._json(404, {"error": "TP non actif sur ce serveur"})
        if path == "/":
            return self._index()
        if path.startswith("/api/"):
            route = ROUTES.get(sha("%s %s" % (self.command if self.command != "HEAD" else "GET", path)))
            if route is None:
                return self._json(404, {"error": "route inconnue"})
            return getattr(self, "_h_" + route["h"])(route, path, body)
        return self._static(path)

    def _index(self):
        tps = sorted(d for d in os.listdir(ROOT)
                     if d.startswith("tp") and os.path.isdir(os.path.join(ROOT, d))
                     and (ONLY is None or d == ONLY))
        links = "".join('<li><a href="/%s/">%s</a></li>' % (t, t) for t in tps)
        self._send(200, "<!doctype html><meta charset=utf-8><title>Labo Jour 2</title>"
                   "<style>body{font-family:system-ui;background:#0b1020;color:#edf2fc;"
                   "max-width:640px;margin:3rem auto;padding:0 1rem}a{color:#7dd3fc}</style>"
                   "<h1>Laboratoire — Jour 2</h1><ul>%s</ul>"
                   "<p><small>127.0.0.1 uniquement — tout est local et simulé.</small></p>" % links,
                   "text/html; charset=utf-8")

    def _static(self, path):
        full = os.path.normpath(os.path.join(ROOT, path.lstrip("/")))
        top = os.path.relpath(full, ROOT).split(os.sep)[0]
        # Seuls les dossiers tpXX sont servis (ni serve.py, ni _lab.json, ni collector.log).
        if not full.startswith(ROOT + os.sep) or not top.startswith("tp") \
                or os.path.basename(full).startswith("_"):
            return self._json(403, {"error": "interdit"})
        if os.path.isdir(full):
            if not path.endswith("/"):
                self.send_response(301)
                self.send_header("Location", path + "/")
                self.end_headers()
                return
            full = os.path.join(full, "index.html")
        if not os.path.isfile(full):
            return self._json(404, {"error": "introuvable"})
        with open(full, "rb") as f:
            data = f.read()
        self._send(200, data, CTYPES.get(os.path.splitext(full)[1].lower(), "application/octet-stream"))

    # -- types de route ----------------------------------------------------
    def _data(self, route):
        return json.loads(unmask(route["data"]))

    def _h_json(self, route, path, body):
        return self._json(200, self._data(route))

    def _h_header_sha(self, route, path, body):
        # Une valeur d'en-tete dont l'empreinte doit correspondre (cle, jeton).
        if sha(self.headers.get(unmask(route["header"]), "")) != route["sha"]:
            return self._json(401, {"error": "authentification refusee"})
        return self._json(200, self._data(route))

    def _h_header_eq(self, route, path, body):
        # Le serveur fait confiance a une valeur fournie par le client (defaut voulu).
        if self.headers.get(unmask(route["header"]), "") != unmask(route["value"]):
            return self._json(403, {"error": "acces refuse"})
        return self._json(200, self._data(route))

    def _h_hmac(self, route, path, body):
        ts = self.headers.get(unmask(route["ts_header"]), "")
        sig = self.headers.get(unmask(route["sig_header"]), "")
        try:
            if abs(time.time() - int(ts)) > route["window"]:
                return self._json(401, {"error": "horodatage hors fenetre"})
        except ValueError:
            return self._json(400, {"error": "horodatage manquant"})
        text = body.decode("utf-8", "replace")
        msg = unmask(route["template"]).format(
            method=self.command, path=path, ts=ts, body=text,
            body_sha256=hashlib.sha256(body).hexdigest())
        mac = hmac.new(unmask(route["key"]).encode(), msg.encode(), hashlib.sha256).digest()
        expect = base64.b64encode(mac).decode() if route["enc"] == "b64" else mac.hex()
        if not hmac.compare_digest(sig, expect):
            return self._json(401, {"error": "signature invalide"})
        try:
            accepted = json.loads(text or "{}")
        except ValueError:
            return self._json(400, {"error": "JSON invalide"})
        out = self._data(route)
        out["accepted"] = accepted
        return self._json(200, out)

    def _h_collect(self, route, path, body):
        # Collecteur de laboratoire : journalise localement, ne renvoie rien d'utile.
        with open(COLLECTOR_LOG, "a", encoding="utf-8") as f:
            f.write("%s %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), body.decode("utf-8", "replace")))
        return self._send(200, b"ok", "text/plain")


def main():
    global ONLY
    port, args, i = 8000, sys.argv[1:], 0
    while i < len(args):
        if args[i] == "--port":
            port = int(args[i + 1])
            i += 2
            continue
        if args[i].startswith("tp"):
            ONLY = args[i]
        i += 1
    if ONLY and not os.path.isdir(os.path.join(ROOT, ONLY)):
        sys.exit("TP inconnu : %s" % ONLY)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("Labo Jour 2 — http://127.0.0.1:%d/%s" % (port, (ONLY + "/") if ONLY else ""))
    print("  127.0.0.1 uniquement. Ctrl-C pour arreter.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nArret.")


if __name__ == "__main__":
    main()
