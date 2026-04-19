# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testmcpserver.py:57
# Component id: sy.source.ass_ade.test_tools_call_unknown
__version__ = "0.1.0"

    def test_tools_call_unknown(self, server: MCPServer):
        _initialize_server(server)
        req = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "nonexistent_tool", "arguments": {}},
        }
        resp = server._handle(req)
        assert resp is not None
        assert resp["result"]["isError"] is True
        assert "Unknown tool" in resp["result"]["content"][0]["text"]
