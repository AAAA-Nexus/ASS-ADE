# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_extended.py:265
# Component id: og.source.ass_ade.testmcp202511features
__version__ = "0.1.0"

class TestMCP202511Features:
    def test_tool_annotations_present_on_workflow_tools(self) -> None:
        for tool in _WORKFLOW_TOOLS:
            assert "annotations" in tool, f"{tool['name']} missing annotations"
            ann = tool["annotations"]
            assert "readOnlyHint" in ann
            assert "destructiveHint" in ann
            assert "idempotentHint" in ann
            assert "openWorldHint" in ann

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

    def test_read_file_is_readonly(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {},
        })
        tools = {t["name"]: t for t in response["result"]["tools"]}
        assert tools["read_file"]["annotations"]["readOnlyHint"] is True
        assert tools["read_file"]["annotations"]["destructiveHint"] is False

    def test_write_file_is_destructive(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {},
        })
        tools = {t["name"]: t for t in response["result"]["tools"]}
        assert tools["write_file"]["annotations"]["destructiveHint"] is True
        assert tools["write_file"]["annotations"]["readOnlyHint"] is False

    def test_run_command_is_open_world(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {},
        })
        tools = {t["name"]: t for t in response["result"]["tools"]}
        assert tools["run_command"]["annotations"]["openWorldHint"] is True

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

    def test_notifications_cancelled_suppresses_no_response(self) -> None:
        """notifications/cancelled has no id — server returns None."""
        server = MCPServer(".")
        response = server._handle({
            "method": "notifications/cancelled",
            "params": {"requestId": 42, "reason": "user cancel"},
        })
        assert response is None

    def test_cancelled_request_returns_error(self) -> None:
        """If a request ID is cancelled before dispatch, tools/call returns -32800."""
        server = MCPServer(".")
        _initialize_server(server)
        # Simulate the client sending a cancel notification first
        server._handle({
            "method": "notifications/cancelled",
            "params": {"requestId": 99},
        })
        # Now the request with that ID arrives
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 99,
            "method": "tools/call",
            "params": {"name": "read_file", "arguments": {"path": "."}},
        })
        assert response is not None
        assert "error" in response
        assert response["error"]["code"] == -32800

    def test_progress_token_extracted_from_meta(self, tmp_path) -> None:
        """_meta.progressToken is accepted in tools/call params without error."""
        # Create the server rooted at tmp_path so the file is within working dir.
        server = MCPServer(str(tmp_path))
        _initialize_server(server)
        # read_file is a builtin tool; it runs synchronously without progress,
        # but the server must accept the _meta field without error.
        test_file = tmp_path / "meta_test.txt"
        test_file.write_text("hello")
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "read_file",
                "arguments": {"path": "meta_test.txt"},
                "_meta": {"progressToken": "tok-1"},
            },
        })
        assert response is not None
        assert response["result"]["isError"] is False
