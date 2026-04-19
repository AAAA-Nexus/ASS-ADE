# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_notifications_cancelled_suppresses_no_response.py:7
# Component id: at.source.a1_at_functions.test_notifications_cancelled_suppresses_no_response
from __future__ import annotations

__version__ = "0.1.0"

def test_notifications_cancelled_suppresses_no_response(self) -> None:
    """notifications/cancelled has no id — server returns None."""
    server = MCPServer(".")
    response = server._handle({
        "method": "notifications/cancelled",
        "params": {"requestId": 42, "reason": "user cancel"},
    })
    assert response is None
