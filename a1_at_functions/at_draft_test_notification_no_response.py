# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_notification_no_response.py:7
# Component id: at.source.a1_at_functions.test_notification_no_response
from __future__ import annotations

__version__ = "0.1.0"

def test_notification_no_response(self, server: MCPServer):
    req = {"method": "notifications/initialized", "params": {}}
    resp = server._handle(req)
    assert resp is None
