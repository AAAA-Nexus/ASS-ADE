"""Tier a2 — assimilated method 'MCPServer._result'

Assimilated from: server.py:1627-1628
"""

from __future__ import annotations


# --- assimilated symbol ---
def _result(req_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}

