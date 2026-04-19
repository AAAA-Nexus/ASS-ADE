# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpserver.py:59
# Component id: sy.source.a4_sy_orchestration.test_tools_call_unknown
from __future__ import annotations

__version__ = "0.1.0"

def test_tools_call_unknown(self, server: MCPServer):
    _initialize_server(server)
    req = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {"name": "nonexistent_tool", "arguments": {}},
    }
    resp = server._handle(req)
    assert resp is not None
    assert resp["result"]["isError"] is True
    assert "Unknown tool" in resp["result"]["content"][0]["text"]
