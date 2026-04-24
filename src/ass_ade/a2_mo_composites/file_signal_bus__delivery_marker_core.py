"""Tier a2 — assimilated method 'FileSignalBus._delivery_marker'

Assimilated from: bus.py:94-96
"""

from __future__ import annotations


# --- assimilated symbol ---
def _delivery_marker(self, sid: str, agent_id: str | None = None) -> Path:
    agent = agent_id or self.agent_id
    return self.root / "read" / _slug(agent) / f"{sid}.delivered"

