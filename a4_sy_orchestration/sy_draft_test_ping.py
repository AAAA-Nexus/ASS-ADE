# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpprotocol.py:20
# Component id: sy.source.a4_sy_orchestration.test_ping
from __future__ import annotations

__version__ = "0.1.0"

def test_ping(self) -> None:
    server = MCPServer(".")
    response = server._handle({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "ping",
        "params": {},
    })
    assert response is not None
    assert response["result"] == {}
