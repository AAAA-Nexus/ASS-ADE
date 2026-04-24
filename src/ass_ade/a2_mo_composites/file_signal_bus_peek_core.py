"""Tier a2 — assimilated method 'FileSignalBus.peek'

Assimilated from: bus.py:171-183
"""

from __future__ import annotations


# --- assimilated symbol ---
def peek(self) -> list[SignalEnvelope]:
    """Like ``unread`` but without marking anything as delivered."""
    now_iso = _rfc3339(self._now())
    out: list[SignalEnvelope] = []
    for env in self.list_inbox():
        if not env.matches(self.agent_id):
            continue
        if env.is_expired(now_iso):
            continue
        if self._delivery_marker(env.signal_id).exists():
            continue
        out.append(env)
    return out

