# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_test_mock_server_serves_manifest.py:7
# Component id: qk.source.a0_qk_constants.test_mock_server_serves_manifest
from __future__ import annotations

__version__ = "0.1.0"

def test_mock_server_serves_manifest() -> None:
    import httpx

    from ass_ade.mcp.mock_server import start_server

    server = start_server(port=19787, block=False)
    try:
        resp = httpx.get("http://127.0.0.1:19787/.well-known/mcp.json", timeout=5)
        assert resp.status_code == 200
        data = resp.json()
        assert "tools" in data
    finally:
        server.shutdown()
