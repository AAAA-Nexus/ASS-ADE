"""Tier a2 — assimilated method 'MCPServer._emit_log'

Assimilated from: server.py:1031-1039
"""

from __future__ import annotations


# --- assimilated symbol ---
def _emit_log(self, level: str, message: str) -> None:
    """Emit a notifications/message log entry (MCP 2025-11-25 logging capability)."""
    self._write(
        {
            "jsonrpc": "2.0",
            "method": "notifications/message",
            "params": {"level": level, "data": message},
        }
    )

