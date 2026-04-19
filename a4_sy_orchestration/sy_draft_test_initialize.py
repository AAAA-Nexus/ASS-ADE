# Extracted from C:/!ass-ade/tests/test_mcp_extended.py:213
# Component id: sy.source.ass_ade.test_initialize
from __future__ import annotations

__version__ = "0.1.0"

def test_initialize(self) -> None:
    server = MCPServer(".")
    response = server._handle({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {},
    })
    assert response is not None
    assert response["result"]["protocolVersion"] == "2025-11-25"
    assert response["result"]["serverInfo"]["version"] == "1.0.0"
