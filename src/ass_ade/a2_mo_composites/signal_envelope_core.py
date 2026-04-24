"""Tier a2 — assimilated class 'SignalEnvelope'

Assimilated from: types.py:63-86
"""

from __future__ import annotations


# --- assimilated symbol ---
class SignalEnvelope:
    """Wire-ready signal: a ``Signal`` plus bus-assigned metadata."""

    signal_id: str
    priority: Priority
    issued_by: str
    issued_at: str      # RFC 3339 UTC, e.g. "2026-04-20T22:30:00Z"
    subject: str
    body: str
    routes: tuple[str, ...]
    ack_required: bool
    expires_at: str
    digest: str         # short sha256, used for tamper-evidence

    def is_expired(self, now_rfc3339: str) -> bool:
        """Pure: compare RFC-3339 strings lexicographically (UTC only)."""
        if not self.expires_at:
            return False
        return now_rfc3339 >= self.expires_at

    def matches(self, agent_id: str) -> bool:
        """Delegate to the protocol-level router (kept pure here by import)."""
        from ass_ade.swarm.protocol import route_matches
        return route_matches(self.routes, agent_id)

