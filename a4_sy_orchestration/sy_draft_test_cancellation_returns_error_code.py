# Extracted from C:/!ass-ade/tests/test_mcp_cancellation.py:117
# Component id: sy.source.ass_ade.test_cancellation_returns_error_code
from __future__ import annotations

__version__ = "0.1.0"

def test_cancellation_returns_error_code(self, server: MCPServer) -> None:
    """Verify that a cancelled request returns the correct error code."""
    _initialize_server(server)

    req_id = 789
    # Simulate a cancellation
    server._cancelled.add(req_id)

    req = {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": "tools/call",
        "params": {"name": "read_file", "arguments": {"path": "hello.py"}},
    }
    resp = server._handle(req)

    assert resp is not None
    assert "error" in resp
    assert resp["error"]["code"] == -32800  # MCP error code for cancellation
