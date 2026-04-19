# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_extended.py:301
# Component id: sy.source.ass_ade.test_write_file_is_destructive
__version__ = "0.1.0"

    def test_write_file_is_destructive(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {},
        })
        tools = {t["name"]: t for t in response["result"]["tools"]}
        assert tools["write_file"]["annotations"]["destructiveHint"] is True
        assert tools["write_file"]["annotations"]["readOnlyHint"] is False
