"""Tier a2 — assimilated class 'DeliveryReceipt'

Assimilated from: types.py:100-114
"""

from __future__ import annotations


# --- assimilated symbol ---
class DeliveryReceipt:
    """Reports what ``FileSignalBus.unread`` returned for a given caller.

    Separate from ``SignalEnvelope`` so tests and callers can reason about
    *which* agent saw *which* signal without threading that context through
    every envelope.
    """

    envelope: SignalEnvelope
    was_delivered_before: bool = False
    delivered_to: str = ""

    def __post_init__(self) -> None:
        if not self.delivered_to:
            object.__setattr__(self, "delivered_to", "anonymous")

