"""Tier a2 — assimilated method 'MCPServer._handle_sync'

Assimilated from: server.py:760-805
"""

from __future__ import annotations


# --- assimilated symbol ---
def _handle_sync(self, request: dict[str, Any]) -> dict[str, Any] | None:
    """Synchronous request handler. Can be called directly from tests or from worker threads.

    Returns the response dict, or None for notifications.
    """
    req_id = request.get("id")
    method = request.get("method", "")
    params = request.get("params") or {}

    # Notifications (no id) — don't respond
    if req_id is None:
        if method == "notifications/initialized":
            self._initialized = True
        elif method == "notifications/cancelled":
            # MCP 2025-11-25: client may cancel an in-flight request
            cancelled_id = params.get("requestId")
            if cancelled_id is not None:
                with self._lock:
                    # Mark as cancelled and try to cancel the future
                    self._cancelled.add(cancelled_id)
                    future = self._futures.get(cancelled_id)
                    if future is not None:
                        # Try to cancel the future if it hasn't started yet
                        future.cancel()
                    # Signal cancellation to the execution context (cooperative cancellation)
                    ctx = self._cancellation_contexts.get(cancelled_id)
                    if ctx is not None:
                        ctx.cancel()
        return None

    NON_INIT_METHODS = {"initialize", "ping", "notifications/initialized"}
    if not self._initialized and method not in NON_INIT_METHODS:
        return self._error(
            req_id, -32002, "Server not initialized. Send 'initialize' first."
        )

    if method == "initialize":
        return self._handle_initialize(req_id, params)
    elif method == "tools/list":
        return self._handle_tools_list(req_id, params)
    elif method == "tools/call":
        return self._handle_tools_call(req_id, params)
    elif method == "ping":
        return self._result(req_id, {})
    else:
        return self._error(req_id, -32601, f"Method not found: {method}")

