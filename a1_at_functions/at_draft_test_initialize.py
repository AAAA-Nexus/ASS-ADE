# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_initialize.py:7
# Component id: at.source.a1_at_functions.test_initialize
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
