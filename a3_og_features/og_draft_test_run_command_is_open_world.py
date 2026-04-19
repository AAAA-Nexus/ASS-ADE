# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testmcp202511features.py:51
# Component id: og.source.ass_ade.test_run_command_is_open_world
__version__ = "0.1.0"

    def test_run_command_is_open_world(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {},
        })
        tools = {t["name"]: t for t in response["result"]["tools"]}
        assert tools["run_command"]["annotations"]["openWorldHint"] is True
