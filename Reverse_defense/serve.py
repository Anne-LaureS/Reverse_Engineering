#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serveur de laboratoire du TP17 (durcissement web). Stdlib uniquement,
127.0.0.1, inoffensif. Il sert les pages statiques et une API /api/export.

La LOGIQUE DE DEFENSE est volontairement sortie dans defense.py (le fichier a
completer). serve.py, lui, ne change pas : il applique les en-tetes de securite
et la validation que defense.py lui fournit.

Usage :
    python serve.py            # sert tp17/ (demo) et tp17/tp/ (groupe)
    python serve.py --port 8000
"""
import argparse
import json
import os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

import defense

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE if os.path.isdir(os.path.join(HERE, "tp17")) else os.path.join(HERE, "distrib")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def end_headers(self):
        for k, v in defense.security_headers().items():
            self.send_header(k, v)
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0].endswith("/api/export"):
            if defense.acces_autorise(self.headers):
                return self._json(200, {"flag": "TP17-EXPORT-OK",
                                        "data": ["ligne1", "ligne2"]})
            return self._json(403, {"error": "acces refuse (validation serveur)"})
        return super().do_GET()

    def log_message(self, *a):
        pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8000)
    args = p.parse_args()
    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print("Lab TP17 sur http://127.0.0.1:%d/  (Ctrl+C pour arreter)" % args.port)
    print("  demo    : http://127.0.0.1:%d/tp17/" % args.port)
    print("  groupe  : http://127.0.0.1:%d/tp17/tp/" % args.port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
