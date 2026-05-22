#!/usr/bin/env python3
"""Static file server for public/ with optional QGIS proxy."""

from __future__ import annotations

import argparse
import http.server
import socketserver
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
QGIS_TARGET = "http://127.0.0.1:8081"


class DevHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def do_OPTIONS(self) -> None:
        if self.path.startswith("/qgis-server"):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header(
                "Access-Control-Allow-Headers",
                "Origin, X-Requested-With, Content-Type, Accept, Authorization",
            )
            self.end_headers()
            return
        super().do_OPTIONS()

    def _proxy_qgis(self, method: str) -> None:
        upstream_path = self.path[len("/qgis-server") :] or "/"
        url = f"{QGIS_TARGET}{upstream_path}"
        body = None
        if method == "POST":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else None
        req = urllib.request.Request(url, data=body, method=method)
        for key in ("Content-Type", "Accept"):
            if key in self.headers:
                req.add_header(key, self.headers[key])
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                payload = resp.read()
                self.send_response(resp.status)
                for key, value in resp.headers.items():
                    if key.lower() not in ("transfer-encoding", "connection"):
                        self.send_header(key, value)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(payload)
        except urllib.error.HTTPError as exc:
            payload = exc.read()
            self.send_response(exc.code)
            self.send_header("Content-Type", exc.headers.get("Content-Type", "text/plain"))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)
        except urllib.error.URLError as exc:
            msg = f"QGIS Server proxy failed ({exc.reason}). Start Docker: docker compose up -d"
            body = msg.encode("utf-8")
            self.send_response(502)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path.startswith("/qgis-server"):
            self._proxy_qgis("GET")
            return
        super().do_GET()

    def do_POST(self) -> None:
        if self.path.startswith("/qgis-server"):
            self._proxy_qgis("POST")
            return
        super().do_POST()


def main() -> int:
    parser = argparse.ArgumentParser(description="Origo dev server (static + QGIS proxy)")
    parser.add_argument("--port", type=int, default=3000)
    args = parser.parse_args()

    if not PUBLIC.is_dir():
        print(f"Missing {PUBLIC}", file=sys.stderr)
        return 1

    with socketserver.ThreadingTCPServer(("", args.port), DevHandler) as httpd:
        print(f"Serving {PUBLIC} at http://localhost:{args.port}")
        print(f"Proxying /qgis-server -> {QGIS_TARGET}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
