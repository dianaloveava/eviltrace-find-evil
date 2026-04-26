from __future__ import annotations

import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .agent import InvestigationAgent, load_run, render_markdown_report
from .evidence import inventory_case, load_events

ROOT = Path(__file__).resolve().parent.parent
WEB_ROOT = ROOT / "web"


class EvilTraceHandler(BaseHTTPRequestHandler):
    server_version = "EvilTrace/0.1"

    def do_GET(self) -> None:  # noqa: N802 - stdlib API
        parsed = urlparse(self.path)
        route = parsed.path
        try:
            if route == "/api/health":
                self._json({"ok": True, "service": "eviltrace"})
            elif route == "/api/evidence":
                evidence = inventory_case("case_alpha")
                events = load_events("case_alpha", evidence)
                self._json({"case_id": "case_alpha", "evidence": [record.__dict__ for record in evidence], "event_count": len(events)})
            elif route == "/api/runs/latest":
                self._json(load_run("latest"))
            elif route.startswith("/api/runs/") and route.endswith("/report.md"):
                run_id = route.removeprefix("/api/runs/").removesuffix("/report.md") or "latest"
                self._text(render_markdown_report(load_run(run_id)), content_type="text/markdown; charset=utf-8")
            elif route.startswith("/api/runs/"):
                run_id = route.removeprefix("/api/runs/") or "latest"
                self._json(load_run(run_id))
            else:
                self._static(route)
        except FileNotFoundError as exc:
            self._json({"error": str(exc)}, status=HTTPStatus.NOT_FOUND)
        except Exception as exc:  # pragma: no cover - defensive HTTP boundary
            self._json({"error": str(exc)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_POST(self) -> None:  # noqa: N802 - stdlib API
        parsed = urlparse(self.path)
        if parsed.path != "/api/runs":
            self._json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)
            return
        try:
            run = InvestigationAgent("case_alpha").run()
            self._json(json.loads(json.dumps(_plain(run))))
        except Exception as exc:  # pragma: no cover - defensive HTTP boundary
            self._json({"error": str(exc)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003 - stdlib signature
        print(f"[eviltrace] {self.address_string()} - {fmt % args}")

    def _json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        raw = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _text(self, body: str, content_type: str = "text/plain; charset=utf-8") -> None:
        raw = body.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _static(self, route: str) -> None:
        route = "/index.html" if route in {"/", ""} else route
        candidate = (WEB_ROOT / route.lstrip("/")).resolve()
        if not str(candidate).startswith(str(WEB_ROOT.resolve())) or not candidate.exists() or not candidate.is_file():
            self._json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)
            return
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        raw = candidate.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def _plain(obj):
    if hasattr(obj, "__dataclass_fields__"):
        return {key: _plain(value) for key, value in obj.__dict__.items()}
    if isinstance(obj, list):
        return [_plain(value) for value in obj]
    if isinstance(obj, dict):
        return {key: _plain(value) for key, value in obj.items()}
    return obj


def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = ThreadingHTTPServer((host, port), EvilTraceHandler)
    print(f"EvilTrace listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
