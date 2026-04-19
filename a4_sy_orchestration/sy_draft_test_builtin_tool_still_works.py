# Extracted from C:/!ass-ade/tests/test_mcp_extended.py:69
# Component id: sy.source.ass_ade.test_builtin_tool_still_works
from __future__ import annotations

__version__ = "0.1.0"

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
