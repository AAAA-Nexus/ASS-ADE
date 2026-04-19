# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testmcp202511features.py:31
# Component id: og.source.ass_ade.test_read_file_is_readonly
__version__ = "0.1.0"

    def test_read_file_is_readonly(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {},
        })
        tools = {t["name"]: t for t in response["result"]["tools"]}
        assert tools["read_file"]["annotations"]["readOnlyHint"] is True
        assert tools["read_file"]["annotations"]["destructiveHint"] is False
