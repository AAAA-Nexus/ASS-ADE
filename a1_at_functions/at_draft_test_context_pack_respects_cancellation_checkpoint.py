# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_context_pack_respects_cancellation_checkpoint.py:7
# Component id: at.source.a1_at_functions.test_context_pack_respects_cancellation_checkpoint
from __future__ import annotations

__version__ = "0.1.0"

def test_context_pack_respects_cancellation_checkpoint(self, server: MCPServer) -> None:
    """Verify that context_pack checks for cancellation."""
    _initialize_server(server)

    from ass_ade.mcp.cancellation import CancellationContext

    req_id = 1001
    args = {"task_description": "test task"}

    # Create a pre-cancelled context
    ctx = CancellationContext()
    ctx.cancel()

    # Call the tool with the cancelled context
    resp = server._call_context_pack(req_id, args, token=None, cancellation_context=ctx)

    # Should return a cancellation error
    assert resp.get("error") is not None
    assert resp["error"]["code"] == -32800
