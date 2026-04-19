# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_cancelled_request_returns_error.py:7
# Component id: at.source.a1_at_functions.test_cancelled_request_returns_error
from __future__ import annotations

__version__ = "0.1.0"

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
