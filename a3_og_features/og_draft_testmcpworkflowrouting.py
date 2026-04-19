# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testmcpworkflowrouting.py:7
# Component id: og.source.a3_og_features.testmcpworkflowrouting
from __future__ import annotations

__version__ = "0.1.0"

class TestMCPWorkflowRouting:
    def test_builtin_tool_still_works(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "list_directory", "arguments": {"path": "."}},
        })
        assert response is not None
        assert "isError" in response["result"]

    def test_unknown_tool_returns_error(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "nonexistent_tool", "arguments": {}},
        })
        assert response is not None
        assert response["result"]["isError"]
