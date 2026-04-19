# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_server_streaming.py:116
# Component id: sy.source.ass_ade.test_notification_no_response
__version__ = "0.1.0"

    def test_notification_no_response(self, server: MCPServer):
        req = {"method": "notifications/initialized", "params": {}}
        resp = server._handle(req)
        assert resp is None
