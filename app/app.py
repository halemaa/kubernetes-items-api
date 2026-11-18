"""
app.py — a tiny items API, standard library only (no pip install needed).

Same idea as the serverless version, but here it runs as a long-lived
container that Kubernetes keeps alive. Endpoints:

    GET  /health   -> liveness/readiness check (used by the k8s probes)
    GET  /items    -> list items
    POST /items    -> add an item   body: {"text": "..."}   header: X-API-Token

Config comes from environment variables, which Kubernetes fills from a
ConfigMap (GREETING, MAX_ITEMS) and a Secret (API_TOKEN). Data is kept
in memory to stay simple — see README for why a real deployment would use
a StatefulSet database or an external store instead.
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

GREETING = os.environ.get("GREETING", "hello from kubernetes")
MAX_ITEMS = int(os.environ.get("MAX_ITEMS", "100"))
API_TOKEN = os.environ.get("API_TOKEN", "")          # injected from the Secret
PORT = int(os.environ.get("PORT", "8080"))

_items = []                                          # in-memory store (per Pod)


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "ok", "greeting": GREETING})
        elif self.path == "/items":
            self._send(200, {"items": _items, "count": len(_items)})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/items":
            return self._send(404, {"error": "not found"})

        # simple token check — the token is provided via the Secret
        if API_TOKEN and self.headers.get("X-API-Token") != API_TOKEN:
            return self._send(401, {"error": "invalid or missing X-API-Token"})

        if len(_items) >= MAX_ITEMS:
            return self._send(429, {"error": f"item limit reached ({MAX_ITEMS})"})

        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._send(400, {"error": "body must be valid JSON"})

        text = (body.get("text") or "").strip()
        if not text:
            return self._send(400, {"error": "field 'text' is required"})

        item = {"id": len(_items) + 1, "text": text}
        _items.append(item)
        self._send(201, item)

    # quieter logs
    def log_message(self, fmt, *args):
        print(f"{self.command} {self.path}")


if __name__ == "__main__":
    print(f"items-api listening on :{PORT}  (max_items={MAX_ITEMS})")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
