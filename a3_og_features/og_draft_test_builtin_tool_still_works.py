# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testmcpworkflowrouting.py:6
# Component id: og.source.ass_ade.test_builtin_tool_still_works
__version__ = "0.1.0"

    def test_builtin_tool_still_works(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "list_directory", "arguments": {"path": "."}},
        })
        assert response is not None
        assert "isError" in response["result"]
