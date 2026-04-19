# Extracted from C:/!ass-ade/tests/test_mcp_extended.py:81
# Component id: sy.source.ass_ade.test_unknown_tool_returns_error
from __future__ import annotations

__version__ = "0.1.0"

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
