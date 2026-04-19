# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_server_streaming.py:121
# Component id: sy.source.ass_ade.test_tools_call_write_file
__version__ = "0.1.0"

    def test_tools_call_write_file(self, server: MCPServer, tmp_path: Path):
        _initialize_server(server)
        req = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {
                "name": "write_file",
                "arguments": {"path": "new.py", "content": "x = 1\n"},
            },
        }
        resp = server._handle(req)
        assert resp["result"]["isError"] is False
        assert (tmp_path / "new.py").read_text() == "x = 1\n"
