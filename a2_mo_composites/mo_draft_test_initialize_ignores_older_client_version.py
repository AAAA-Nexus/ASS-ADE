# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_extended.py:249
# Component id: mo.source.ass_ade.test_initialize_ignores_older_client_version
__version__ = "0.1.0"

    def test_initialize_ignores_older_client_version(self) -> None:
        """Server always responds with its own version regardless of client request."""
        server = MCPServer(".")
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2024-11-05"},
        })
        assert response is not None
        assert response["result"]["protocolVersion"] == "2025-11-25"
