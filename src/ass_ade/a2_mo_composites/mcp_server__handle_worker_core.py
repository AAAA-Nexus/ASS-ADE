"""Tier a2 — assimilated method 'MCPServer._handle_worker'

Assimilated from: server.py:739-758
"""

from __future__ import annotations


# --- assimilated symbol ---
def _handle_worker(self, request: dict[str, Any]) -> None:
    """Worker thread entry point. Calls _handle_sync and writes the response.

    Runs in the thread pool executor. Handles any exceptions and ensures
    the response is written with proper serialization via _write_lock.
    """
    req_id = request.get("id")
    try:
        response = self._handle_sync(request)
        if response is not None:
            self._write(response)
    except (AttributeError, ImportError, LookupError, OSError, RuntimeError, TypeError, ValueError):
        _LOG.exception("Request handler failed: id=%s", req_id)
        if req_id is not None:
            self._write(self._error(req_id, -32603, "Internal server error"))
    finally:
        # Clean up the future reference
        if req_id is not None:
            with self._lock:
                self._futures.pop(req_id, None)

