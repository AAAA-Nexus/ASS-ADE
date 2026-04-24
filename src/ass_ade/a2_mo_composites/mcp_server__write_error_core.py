"""Tier a2 — assimilated method 'MCPServer._write_error'

Assimilated from: server.py:1644-1645
"""

from __future__ import annotations


# --- assimilated symbol ---
def _write_error(self, req_id: Any, code: int, message: str) -> None:
    self._write(self._error(req_id, code, message))

