# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpserver.py:86
# Component id: sy.source.a4_sy_orchestration.test_notification_no_response
from __future__ import annotations

__version__ = "0.1.0"

def test_notification_no_response(self, server: MCPServer):
    req = {"method": "notifications/initialized", "params": {}}
    resp = server._handle(req)
    assert resp is None
