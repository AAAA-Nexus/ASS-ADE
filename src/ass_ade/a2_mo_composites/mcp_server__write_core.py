"""Tier a2 — assimilated method 'MCPServer._write'

Assimilated from: server.py:1638-1642
"""

from __future__ import annotations


# --- assimilated symbol ---
def _write(self, message: dict[str, Any]) -> None:
    data = json.dumps(message) + "\n"
    with self._write_lock:
        sys.stdout.write(data)
        sys.stdout.flush()

