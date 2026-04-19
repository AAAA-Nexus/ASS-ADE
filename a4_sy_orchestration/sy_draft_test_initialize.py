# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpserver.py:13
# Component id: sy.source.a4_sy_orchestration.test_initialize
from __future__ import annotations

__version__ = "0.1.0"

def test_initialize(self, server: MCPServer):
    req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    resp = server._handle(req)
    assert resp is not None
    assert resp["id"] == 1
    result = resp["result"]
    assert result["protocolVersion"] == "2025-11-25"
    assert result["serverInfo"]["name"] == "ass-ade"
    assert "tools" in result["capabilities"]
