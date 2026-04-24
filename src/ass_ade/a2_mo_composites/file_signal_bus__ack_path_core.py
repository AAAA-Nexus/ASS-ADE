"""Tier a2 — assimilated method 'FileSignalBus._ack_path'

Assimilated from: bus.py:98-100
"""

from __future__ import annotations


# --- assimilated symbol ---
def _ack_path(self, sid: str, agent_id: str | None = None) -> Path:
    agent = agent_id or self.agent_id
    return self.root / "acks" / _slug(agent) / f"{sid}.ack.md"

