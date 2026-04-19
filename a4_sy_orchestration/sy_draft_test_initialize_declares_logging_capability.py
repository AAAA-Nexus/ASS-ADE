# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpprotocol.py:31
# Component id: sy.source.a4_sy_orchestration.test_initialize_declares_logging_capability
from __future__ import annotations

__version__ = "0.1.0"

def test_initialize_declares_logging_capability(self) -> None:
    server = MCPServer(".")
    response = server._handle({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {"protocolVersion": "2025-11-25"},
    })
    assert response is not None
    caps = response["result"]["capabilities"]
    assert "logging" in caps
    assert "tools" in caps
