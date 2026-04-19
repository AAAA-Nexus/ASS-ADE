# Extracted from C:/!ass-ade/tests/test_mcp.py:110
# Component id: sy.source.ass_ade.handler
from __future__ import annotations

__version__ = "0.1.0"

def handler(request: httpx.Request) -> httpx.Response:
    captured["authorization"] = request.headers.get("Authorization", "")
    captured["x_api_key"] = request.headers.get("X-API-Key", "")
    return httpx.Response(200, json={"ok": True})
