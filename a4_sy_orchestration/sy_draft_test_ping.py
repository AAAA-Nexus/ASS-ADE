# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_server_streaming.py:110
# Component id: sy.source.ass_ade.test_ping
__version__ = "0.1.0"

    def test_ping(self, server: MCPServer):
        req = {"jsonrpc": "2.0", "id": 6, "method": "ping", "params": {}}
        resp = server._handle(req)
        assert resp is not None
        assert resp["result"] == {}
