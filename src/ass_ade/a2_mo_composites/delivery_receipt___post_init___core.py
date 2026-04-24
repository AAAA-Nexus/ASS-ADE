"""Tier a2 — assimilated method 'DeliveryReceipt.__post_init__'

Assimilated from: types.py:112-114
"""

from __future__ import annotations


# --- assimilated symbol ---
def __post_init__(self) -> None:
    if not self.delivered_to:
        object.__setattr__(self, "delivered_to", "anonymous")

