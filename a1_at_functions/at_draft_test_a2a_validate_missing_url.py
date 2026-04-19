# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testmcpa2avalidate.py:28
# Component id: at.source.a1_at_functions.test_a2a_validate_missing_url
from __future__ import annotations

__version__ = "0.1.0"

def test_a2a_validate_missing_url(self) -> None:
    server = MCPServer(".")
    _initialize_server(server)
    response = server._handle({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "a2a_validate", "arguments": {"url": ""}},
    })
    assert response is not None
    assert response["error"]["code"] == -32602
