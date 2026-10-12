"""Dev/browser-server: statische ui + json-api auf http://127.0.0.1:8765."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .api import Api

UI_DIR = os.path.join(os.path.dirname(__file__), "ui")
HOST, PORT = "127.0.0.1", 8765

_api = Api()


class Handler(BaseHTTPRequestHandler):
    server_version = "PythonLearner/1.0"

    def log_message(self, fmt, *args):  # konsole sauber halten
        pass

    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if not self.path.startswith("/api/"):
            self.send_error(404)
            return
        method = self.path[len("/api/"):]
        fn = getattr(_api, method, None)
        if fn is None or method.startswith("_"):
            self._send_json({"error": f"unknown method {method}"}, 404)
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
            params = json.loads(self.rfile.read(length) or b"{}")
            self._send_json(fn(params))
        except Exception as e:  # fehler ans ui melden statt einfach zu hängen
            self._send_json({"error": f"{type(e).__name__}: {e}"}, 500)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/" or path == "":
            path = "/index.html"
        # gegen path traversal, sonst kommt man ausm ui-ordner raus
        rel = os.path.normpath(path.lstrip("/\\"))
        if rel.startswith("..") or os.path.isabs(rel):
            self.send_error(403)
            return
        full = os.path.join(UI_DIR, rel)
        if not os.path.isfile(full):
            self.send_error(404)
            return
        ctype = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json; charset=utf-8",
        }.get(os.path.splitext(full)[1].lower(), "application/octet-stream")
        with open(full, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def main():
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Python Learner dev server running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
