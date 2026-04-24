"""Tier a2 — assimilated method 'SwarmCoordinator.announce'

Assimilated from: coordinator.py:97-110
"""

from __future__ import annotations


# --- assimilated symbol ---
def announce(
    self,
    subject: str,
    body: str,
    *,
    routes: Iterable[str] = ("*",),
) -> SignalEnvelope:
    return self.bus.broadcast(Signal(
        priority=Priority.P2_INFORM,
        subject=subject,
        body=body,
        routes=tuple(routes),
        issued_by=self.bus.agent_id,
    ))

