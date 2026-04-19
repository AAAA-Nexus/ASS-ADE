# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testmcp202511features.py:15
# Component id: og.source.ass_ade.test_tools_list_includes_annotations_for_builtin_tools
__version__ = "0.1.0"

    def test_tools_list_includes_annotations_for_builtin_tools(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {},
        })
        assert response is not None
        tools = {t["name"]: t for t in response["result"]["tools"]}

        for name in ("read_file", "write_file", "edit_file", "run_command",
                     "list_directory", "search_files", "grep_search"):
            assert "annotations" in tools[name], f"{name} missing annotations"
