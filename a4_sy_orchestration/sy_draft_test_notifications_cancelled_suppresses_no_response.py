# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_extended.py:334
# Component id: sy.source.ass_ade.test_notifications_cancelled_suppresses_no_response
__version__ = "0.1.0"

    def test_notifications_cancelled_suppresses_no_response(self) -> None:
        """notifications/cancelled has no id — server returns None."""
        server = MCPServer(".")
        response = server._handle({
            "method": "notifications/cancelled",
            "params": {"requestId": 42, "reason": "user cancel"},
        })
        assert response is None
