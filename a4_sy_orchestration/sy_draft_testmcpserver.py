# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpserver.py:7
# Component id: sy.source.a4_sy_orchestration.testmcpserver
from __future__ import annotations

__version__ = "0.1.0"

class TestMCPServer:
    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        (tmp_path / "hello.py").write_text("print('hi')\n")
        return MCPServer(working_dir=str(tmp_path))

    def test_initialize(self, server: MCPServer):
        req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        resp = server._handle(req)
        assert resp is not None
        assert resp["id"] == 1
        result = resp["result"]
        assert result["protocolVersion"] == "2025-11-25"
        assert result["serverInfo"]["name"] == "ass-ade"
        assert "tools" in result["capabilities"]

    def test_tools_list(self, server: MCPServer):
        _initialize_server(server)
        req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        resp = server._handle(req)
        assert resp is not None
        tools = resp["result"]["tools"]
        names = {t["name"] for t in tools}
        assert "read_file" in names
        assert "write_file" in names
        assert "edit_file" in names
        assert "run_command" in names
        assert "list_directory" in names
        assert "search_files" in names
        assert "grep_search" in names
        assert "phase0_recon" in names
        assert "context_pack" in names
        assert "context_memory_store" in names
        assert "context_memory_query" in names
        assert "map_terrain" in names
        # Verify minimum expected tools; exact count may vary with additional tools
        assert len(tools) >= 19  # At least 8 builtin + 11 workflow/agent/A2A

    def test_tools_call_read_file(self, server: MCPServer):
        _initialize_server(server)
        req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "read_file", "arguments": {"path": "hello.py"}},
        }
        resp = server._handle(req)
        assert resp is not None
        assert resp["result"]["isError"] is False
        content = resp["result"]["content"][0]["text"]
        assert "print('hi')" in content

    def test_tools_call_unknown(self, server: MCPServer):
        _initialize_server(server)
        req = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "nonexistent_tool", "arguments": {}},
        }
        resp = server._handle(req)
        assert resp is not None
        assert resp["result"]["isError"] is True
        assert "Unknown tool" in resp["result"]["content"][0]["text"]

    def test_unknown_method(self, server: MCPServer):
        _initialize_server(server)
        req = {"jsonrpc": "2.0", "id": 5, "method": "weird/method", "params": {}}
        resp = server._handle(req)
        assert resp is not None
        assert "error" in resp
        assert resp["error"]["code"] == -32601

    def test_ping(self, server: MCPServer):
        req = {"jsonrpc": "2.0", "id": 6, "method": "ping", "params": {}}
        resp = server._handle(req)
        assert resp is not None
        assert resp["result"] == {}

    def test_notification_no_response(self, server: MCPServer):
        req = {"method": "notifications/initialized", "params": {}}
        resp = server._handle(req)
        assert resp is None

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

    def test_tools_call_list_directory(self, server: MCPServer):
        _initialize_server(server)
        req = {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "tools/call",
            "params": {"name": "list_directory", "arguments": {}},
        }
        resp = server._handle(req)
        assert resp["result"]["isError"] is False
        assert "hello.py" in resp["result"]["content"][0]["text"]
