# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_builtin_tool_still_works.py:7
# Component id: at.source.a1_at_functions.test_builtin_tool_still_works
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
