# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testmcpserver.py:11
# Component id: sy.source.ass_ade.test_initialize
__version__ = "0.1.0"

    def test_initialize(self, server: MCPServer):
        req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        resp = server._handle(req)
        assert resp is not None
        assert resp["id"] == 1
        result = resp["result"]
        assert result["protocolVersion"] == "2025-11-25"
        assert result["serverInfo"]["name"] == "ass-ade"
        assert "tools" in result["capabilities"]
