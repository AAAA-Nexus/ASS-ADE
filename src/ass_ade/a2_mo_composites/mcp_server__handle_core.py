"""Tier a2 — assimilated method 'MCPServer._handle'

Assimilated from: server.py:807-813
"""

from __future__ import annotations


# --- assimilated symbol ---
def _handle(self, request: dict[str, Any]) -> dict[str, Any] | None:
    """Public request handler. Delegates to _handle_sync for synchronous execution.

    Used by tests and any callers that expect synchronous responses.
    In production (run() method), requests are dispatched via thread pool instead.
    """
    return self._handle_sync(request)

