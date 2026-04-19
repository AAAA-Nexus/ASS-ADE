# Extracted from C:/!ass-ade/tests/test_mcp_cancellation.py:177
# Component id: sy.source.ass_ade.test_concurrent_cancellation_scenario
from __future__ import annotations

__version__ = "0.1.0"

def test_concurrent_cancellation_scenario(self, server: MCPServer) -> None:
    """Test cancellation in a concurrent scenario."""
    _initialize_server(server)

    from ass_ade.mcp.cancellation import CancellationContext

    req_id = 1002
    ctx = CancellationContext()

    def delayed_cancel():
        time.sleep(0.05)
        ctx.cancel()

    # Start a thread that cancels after a delay
    cancel_thread = threading.Thread(target=delayed_cancel)
    cancel_thread.start()

    # Simulate a long-running operation checking for cancellation
    start_time = time.time()
    while not ctx.check():
        time.sleep(0.01)
    elapsed = time.time() - start_time

    cancel_thread.join()

    # Should have taken roughly 50ms (the delay), not much more
    assert 0.04 < elapsed < 0.2
