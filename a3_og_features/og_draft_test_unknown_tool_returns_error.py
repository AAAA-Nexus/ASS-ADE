# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testmcpworkflowrouting.py:18
# Component id: og.source.ass_ade.test_unknown_tool_returns_error
__version__ = "0.1.0"

    def test_unknown_tool_returns_error(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "nonexistent_tool", "arguments": {}},
        })
        assert response is not None
        assert response["result"]["isError"]
