# Extracted from C:/!ass-ade/tests/test_mcp_server_streaming.py:89
# Component id: sy.source.ass_ade.test_tools_call_unknown
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
