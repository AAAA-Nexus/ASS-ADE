# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_extended.py:320
# Component id: sy.source.ass_ade.test_tools_list_accepts_cursor_param
__version__ = "0.1.0"

    def test_tools_list_accepts_cursor_param(self) -> None:
        """Cursor is accepted; all tools returned in single page with no nextCursor."""
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {"cursor": "some-cursor"},
        })
        assert response is not None
        assert "tools" in response["result"]
        assert "nextCursor" not in response["result"]
