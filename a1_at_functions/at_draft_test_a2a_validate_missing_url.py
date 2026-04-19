# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_extended.py:121
# Component id: at.source.ass_ade.test_a2a_validate_missing_url
__version__ = "0.1.0"

    def test_a2a_validate_missing_url(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "a2a_validate", "arguments": {"url": ""}},
        })
        assert response is not None
        assert response["error"]["code"] == -32602
