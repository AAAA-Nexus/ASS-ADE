# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_tools_call_list_directory.py:7
# Component id: at.source.a1_at_functions.test_tools_call_list_directory
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
