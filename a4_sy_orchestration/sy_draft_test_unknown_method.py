# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_server_streaming.py:102
# Component id: sy.source.ass_ade.test_unknown_method
__version__ = "0.1.0"

    def test_unknown_method(self, server: MCPServer):
        _initialize_server(server)
        req = {"jsonrpc": "2.0", "id": 5, "method": "weird/method", "params": {}}
        resp = server._handle(req)
        assert resp is not None
        assert "error" in resp
        assert resp["error"]["code"] == -32601
