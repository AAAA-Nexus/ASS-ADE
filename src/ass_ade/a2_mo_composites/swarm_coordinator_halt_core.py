"""Tier a2 — assimilated method 'SwarmCoordinator.halt'

Assimilated from: coordinator.py:129-143
"""

from __future__ import annotations


# --- assimilated symbol ---
def halt(
    self,
    subject: str,
    body: str,
    *,
    routes: Iterable[str],
) -> SignalEnvelope:
    return self.bus.broadcast(Signal(
        priority=Priority.P0_HALT,
        subject=subject,
        body=body,
        routes=tuple(routes),
        ack_required=True,
        issued_by=self.bus.agent_id,
    ))

