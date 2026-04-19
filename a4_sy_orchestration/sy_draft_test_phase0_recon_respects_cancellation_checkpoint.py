# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpcancellation.py:72
# Component id: sy.source.a4_sy_orchestration.test_phase0_recon_respects_cancellation_checkpoint
from __future__ import annotations

__version__ = "0.1.0"

def test_phase0_recon_respects_cancellation_checkpoint(self, server: MCPServer) -> None:
    """Verify that phase0_recon checks for cancellation."""
    _initialize_server(server)

    from ass_ade.mcp.cancellation import CancellationContext

    req_id = 999
    args = {"task_description": "test task"}

    # Create a pre-cancelled context
    ctx = CancellationContext()
    ctx.cancel()

    # Call the tool with the cancelled context
    resp = server._call_phase0_recon(req_id, args, token=None, cancellation_context=ctx)

    # Should return a cancellation error
    assert resp.get("error") is not None
    assert resp["error"]["code"] == -32800
