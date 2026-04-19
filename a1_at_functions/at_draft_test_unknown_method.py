# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_unknown_method.py:7
# Component id: at.source.a1_at_functions.test_unknown_method
from __future__ import annotations

__version__ = "0.1.0"

def test_unknown_method(self, server: MCPServer):
    _initialize_server(server)
    req = {"jsonrpc": "2.0", "id": 5, "method": "weird/method", "params": {}}
    resp = server._handle(req)
    assert resp is not None
    assert "error" in resp
    assert resp["error"]["code"] == -32601
