"""Tier a2 — assimilated method 'SwarmCoordinator.reroute'

Assimilated from: coordinator.py:112-127
"""

from __future__ import annotations


# --- assimilated symbol ---
def reroute(
    self,
    subject: str,
    body: str,
    *,
    routes: Iterable[str],
    ack_required: bool = True,
) -> SignalEnvelope:
    return self.bus.broadcast(Signal(
        priority=Priority.P1_REROUTE,
        subject=subject,
        body=body,
        routes=tuple(routes),
        ack_required=ack_required,
        issued_by=self.bus.agent_id,
    ))

