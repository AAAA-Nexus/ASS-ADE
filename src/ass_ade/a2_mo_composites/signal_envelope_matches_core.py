"""Tier a2 — assimilated method 'SignalEnvelope.matches'

Assimilated from: types.py:83-86
"""

from __future__ import annotations


# --- assimilated symbol ---
def matches(self, agent_id: str) -> bool:
    """Delegate to the protocol-level router (kept pure here by import)."""
    from ass_ade.swarm.protocol import route_matches
    return route_matches(self.routes, agent_id)

