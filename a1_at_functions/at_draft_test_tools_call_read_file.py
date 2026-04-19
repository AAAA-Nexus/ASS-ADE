# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_tools_call_read_file.py:7
# Component id: at.source.a1_at_functions.test_tools_call_read_file
from __future__ import annotations

__version__ = "0.1.0"

def test_tools_call_read_file(self, server: MCPServer):
    _initialize_server(server)
    req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "read_file", "arguments": {"path": "hello.py"}},
    }
    resp = server._handle(req)
    assert resp is not None
    assert resp["result"]["isError"] is False
    content = resp["result"]["content"][0]["text"]
    assert "print('hi')" in content
