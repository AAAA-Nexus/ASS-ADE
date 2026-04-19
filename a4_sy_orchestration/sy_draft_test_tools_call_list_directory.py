# Extracted from C:/!ass-ade/tests/test_mcp_server_streaming.py:136
# Component id: sy.source.ass_ade.test_tools_call_list_directory
from __future__ import annotations

__version__ = "0.1.0"

def test_tools_call_list_directory(self, server: MCPServer):
    _initialize_server(server)
    req = {
        "jsonrpc": "2.0",
        "id": 8,
        "method": "tools/call",
        "params": {"name": "list_directory", "arguments": {}},
    }
    resp = server._handle(req)
    assert resp["result"]["isError"] is False
    assert "hello.py" in resp["result"]["content"][0]["text"]
