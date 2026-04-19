# Extracted from C:/!ass-ade/tests/test_mcp.py:275
# Component id: sy.source.ass_ade.test_mock_server_oversized_body_returns_413_with_content_length
from __future__ import annotations

__version__ = "0.1.0"

def test_mock_server_oversized_body_returns_413_with_content_length() -> None:
    import httpx

    from ass_ade.mcp.mock_server import _MAX_BODY_BYTES, start_server

    server = start_server(port=19788, block=False)
    try:
        payload = b"x" * (_MAX_BODY_BYTES + 1)
        resp = httpx.post(
            "http://127.0.0.1:19788/tools/echo",
            content=payload,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        assert resp.status_code == 413
        assert "Content-Length" in resp.headers
        assert int(resp.headers["Content-Length"]) == len(resp.content)
        assert resp.json()["error"] == "request entity too large"
    finally:
        server.shutdown()
