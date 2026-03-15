import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from feedback_engine import analyze_chat_session


WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = WORKSPACE_ROOT / "frontend"
HOST = os.getenv("CHATTIME_HOST", "0.0.0.0")
PORT = int(os.getenv("CHATTIME_PORT", "8000"))


class ChatTimeHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, file_path: Path):
        if not file_path.exists() or not file_path.is_file():
            self._send_json(404, {"error": "Not found"})
            return

        mime_type, _ = mimetypes.guess_type(str(file_path))
        content_type = mime_type or "application/octet-stream"
        data = file_path.read_bytes()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _safe_frontend_file(self, request_path: str):
        requested = request_path.lstrip("/") or "chattime.html"
        candidate = (FRONTEND_DIR / requested).resolve()
        if FRONTEND_DIR.resolve() not in candidate.parents and candidate != FRONTEND_DIR.resolve():
            return None
        return candidate

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path == "/health":
            self._send_json(200, {"status": "ok"})
            return

        if path == "/":
            self._send_file(FRONTEND_DIR / "chattime.html")
            return

        file_path = self._safe_frontend_file(path)
        if file_path and file_path.exists():
            self._send_file(file_path)
            return

        self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path != "/api/feedback":
            self._send_json(404, {"error": "Not found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"

        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON payload"})
            return

        prompts = payload.get("prompts", [])
        if not isinstance(prompts, list):
            self._send_json(400, {"error": "'prompts' must be an array of strings"})
            return

        try:
            analysis = analyze_chat_session(prompts)
            self._send_json(200, analysis)
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})
        except Exception as exc:
            self._send_json(500, {"error": f"Failed to analyze session: {exc}"})


def run_server():
    server = ThreadingHTTPServer((HOST, PORT), ChatTimeHandler)
    print(f"ChatTime server running on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()