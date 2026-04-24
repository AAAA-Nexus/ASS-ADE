"""Lightweight MCP mock server for local development.

Serves a configurable MCP manifest at ``/.well-known/mcp.json`` and echoes
JSON payloads back for any configured tool endpoint. No external dependencies
are required beyond the Python standard library and httpx.

Usage (from the CLI via ``ass-ade mcp mock-server``):

    ass-ade mcp mock-server --manifest examples/ass-ade.config.json --port 8787
"""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

_MAX_BODY_BYTES = 1 * 1024 * 1024  # 1 MB

_DEFAULT_MANIFEST = {
    "name": "mock-nexus",
    "version": "0.0.0",
    "mcpVersion": "2025-11-25",
    "serverUrl": "http://localhost:8787",
    "tools": [
        {
            "name": "echo",
            "endpoint": "/tools/echo",
            "method": "POST",
            "paid": False,
        }
    ],
}


class _Handler(BaseHTTPRequestHandler):
    manifest: dict = _DEFAULT_MANIFEST

    def log_message(self, fmt: str, *args: Any) -> None:  # silence stdlib logging
        pass

    def _send_json(self, code: int, body: Any) -> None:
        data = json.dumps(body, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/.well-known/mcp.json", "/mcp.json"):
            self._send_json(200, self.manifest)
        elif self.path == "/health":
            self._send_json(200, {"status": "ok", "version": "mock"})
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        try:
            raw_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(400, {"error": "invalid Content-Length"})
            return
        if raw_length > _MAX_BODY_BYTES:
            # Drain the announced body so the connection can be closed cleanly.
            remaining = raw_length
            while remaining > 0:
                chunk = self.rfile.read(min(65536, remaining))
                if not chunk:
                    break
                remaining -= len(chunk)
            self._send_json(413, {"error": "request entity too large"})
            return
        length = raw_length
        body: Any = {}
        if length:
            try:
                body = json.loads(self.rfile.read(length).decode("utf-8"))
            except Exception:
                self._send_json(400, {"error": "invalid JSON"})
                return
        # Echo back the payload with the matched path
        self._send_json(200, {"echo": body, "path": self.path})


def build_handler(manifest: dict) -> type[_Handler]:
    """Return a handler class with the given manifest bound."""
    class BoundHandler(_Handler):
        pass
    BoundHandler.manifest = manifest
    return BoundHandler


def start_server(
    port: int = 8787,
    *,
    manifest_path: Path | None = None,
    block: bool = True,
) -> HTTPServer | None:
    """Start the mock server.

    Returns the ``HTTPServer`` instance. When ``block=False`` the server
    runs in a daemon thread so it stops automatically when the process exits.
    """
    manifest = _DEFAULT_MANIFEST.copy()
    if manifest_path is not None and manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            pass  # fall back to default manifest

    handler_cls = build_handler(manifest)
    server = HTTPServer(("127.0.0.1", port), handler_cls)

    if not block:
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        return server

    server.serve_forever()
    return None
