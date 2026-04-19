# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_a2a_negotiate_invalid_remote.py:7
# Component id: at.source.a1_at_functions.test_a2a_negotiate_invalid_remote
from __future__ import annotations

__version__ = "0.1.0"

def test_a2a_negotiate_invalid_remote(self) -> None:
    import httpx as _httpx

    server = MCPServer(".")
    _initialize_server(server)
    with patch("ass_ade.a2a.httpx.get", side_effect=_httpx.ConnectError("refused")):
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "a2a_negotiate", "arguments": {"remote_url": "https://bad.com"}},
        })

    assert response is not None
    assert response["result"]["isError"]
