"""Tier a2 — assimilated method 'MCPServer._emit_progress'

Assimilated from: server.py:1008-1029
"""

from __future__ import annotations


# --- assimilated symbol ---
def _emit_progress(
    self,
    token: Any,
    progress: float,
    total: float = 1.0,
    message: str = "",
) -> None:
    """Emit a notifications/progress message if a progress token was provided."""
    if token is None:
        return
    notification: dict[str, Any] = {
        "jsonrpc": "2.0",
        "method": "notifications/progress",
        "params": {
            "progressToken": token,
            "progress": progress,
            "total": total,
        },
    }
    if message:
        notification["params"]["message"] = message
    self._write(notification)

