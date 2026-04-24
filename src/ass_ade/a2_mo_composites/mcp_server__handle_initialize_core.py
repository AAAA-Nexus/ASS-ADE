"""Tier a2 — assimilated method 'MCPServer._handle_initialize'

Assimilated from: server.py:815-832
"""

from __future__ import annotations


# --- assimilated symbol ---
def _handle_initialize(self, req_id: Any, _params: dict[str, Any]) -> dict[str, Any]:
    # MCP 2025-11-25: always respond with our supported version.
    # The client's requested version (params.get("protocolVersion")) is
    # informational; we do not downgrade.
    return self._result(
        req_id,
        {
            "protocolVersion": self.PROTOCOL_VERSION,
            "capabilities": {
                "logging": {},
                "tools": {"listChanged": False},
            },
            "serverInfo": {
                "name": self.SERVER_NAME,
                "version": self.SERVER_VERSION,
            },
        },
    )

