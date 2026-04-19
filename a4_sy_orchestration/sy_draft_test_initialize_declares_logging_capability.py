# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_extended.py:236
# Component id: sy.source.ass_ade.test_initialize_declares_logging_capability
__version__ = "0.1.0"

    def test_initialize_declares_logging_capability(self) -> None:
        server = MCPServer(".")
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2025-11-25"},
        })
        assert response is not None
        caps = response["result"]["capabilities"]
        assert "logging" in caps
        assert "tools" in caps
