"""Tier a2 — assimilated class 'TickResult'

Assimilated from: coordinator.py:35-48
"""

from __future__ import annotations


# --- assimilated symbol ---
class TickResult:
    """Outcome of one coordinator tick. Controllers can branch on this."""

    delivered: list[DeliveryReceipt]
    halt_signals: list[SignalEnvelope]
    reroute_signals: list[SignalEnvelope]

    @property
    def must_halt(self) -> bool:
        return bool(self.halt_signals)

    @property
    def should_reroute(self) -> bool:
        return bool(self.reroute_signals)

