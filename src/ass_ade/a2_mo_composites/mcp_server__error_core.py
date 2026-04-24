"""Tier a2 — assimilated method 'MCPServer._error'

Assimilated from: server.py:1631-1636
"""

from __future__ import annotations


# --- assimilated symbol ---
def _error(req_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": code, "message": message},
    }

