# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testmcp202511features.py:62
# Component id: og.source.a3_og_features.test_tools_list_accepts_cursor_param
from __future__ import annotations

__version__ = "0.1.0"

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
