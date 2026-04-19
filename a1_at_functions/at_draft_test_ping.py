# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_ping.py:7
# Component id: at.source.a1_at_functions.test_ping
from __future__ import annotations

__version__ = "0.1.0"

def test_ping(self, server: MCPServer):
    req = {"jsonrpc": "2.0", "id": 6, "method": "ping", "params": {}}
    resp = server._handle(req)
    assert resp is not None
    assert resp["result"] == {}
