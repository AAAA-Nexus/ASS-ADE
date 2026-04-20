"""Tests for MCP cancellation behavior with cooperative cancellation support."""

from __future__ import annotations

import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ass_ade.mcp.cancellation import CancellationContext, NullCancellationContext
from ass_ade.mcp.server import MCPServer


def _initialize_server(server: MCPServer) -> None:
    response = server._handle({
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {},
    })
    assert response is not None
    server._handle({"method": "notifications/initialized", "params": {}})


class TestCancellationContext:
    """Test basic cancellation context behavior."""

    def test_cancellation_context_defaults_to_not_cancelled(self) -> None:
        ctx = CancellationContext()
        assert ctx.check() is False
        assert ctx.is_cancelled is False

    def test_cancellation_context_can_be_marked_cancelled(self) -> None:
        ctx = CancellationContext()
        ctx.cancel()
        assert ctx.check() is True
        assert ctx.is_cancelled is True

    def test_null_cancellation_context_never_cancels(self) -> None:
        ctx = NullCancellationContext()
        ctx.cancel()
        assert ctx.check() is False
        assert ctx.is_cancelled is False

    def test_cancellation_context_is_thread_safe(self) -> None:
        ctx = CancellationContext()
        results = []

        def check_many_times():
            for _ in range(100):
                results.append(ctx.check())
                time.sleep(0.001)

        def cancel_once():
            time.sleep(0.01)
            ctx.cancel()

        threads = [threading.Thread(target=check_many_times) for _ in range(5)]
        threads.append(threading.Thread(target=cancel_once))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should have some False and some True values
        assert False in results
        assert True in results


class TestMCPCancellation:
    """Test MCP server cancellation behavior."""

    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        (tmp_path / "hello.py").write_text("print('hi')\n")
        return MCPServer(working_dir=str(tmp_path))

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

    def test_cancellation_notification_marks_context_cancelled(self, server: MCPServer) -> None:
        """Verify that notifications/cancelled marks the context as cancelled."""
        _initialize_server(server)

        req_id = 456
        # Create a cancellation context by starting a request
        # (in practice, the server._handle_tools_call creates it)
        ctx = server._cancellation_contexts[req_id] = CancellationContext()

        # Send a cancellation notification
        cancel_notif = {
            "method": "notifications/cancelled",
            "params": {"requestId": req_id},
        }
        server._handle(cancel_notif)

        # The context should now be marked as cancelled
        assert ctx.check() is True

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
