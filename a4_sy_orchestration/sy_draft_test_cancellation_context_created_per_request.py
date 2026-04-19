# Extracted from C:/!ass-ade/tests/test_mcp_cancellation.py:80
# Component id: sy.source.ass_ade.test_cancellation_context_created_per_request
from __future__ import annotations

__version__ = "0.1.0"

def test_cancellation_context_created_per_request(self, server: MCPServer) -> None:
    """Verify that a cancellation context is created for each request."""
    _initialize_server(server)

    # Start a simple request
    req = {
        "jsonrpc": "2.0",
        "id": 123,
        "method": "tools/call",
        "params": {"name": "read_file", "arguments": {"path": "hello.py"}},
    }
    resp = server._handle(req)
    assert resp is not None
    assert resp["result"]["isError"] is False

    # The cancellation context should have been cleaned up
    assert 123 not in server._cancellation_contexts
