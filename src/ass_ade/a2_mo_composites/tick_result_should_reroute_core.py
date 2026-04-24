"""Tier a2 — assimilated method 'TickResult.should_reroute'

Assimilated from: coordinator.py:47-48
"""

from __future__ import annotations


# --- assimilated symbol ---
def should_reroute(self) -> bool:
    return bool(self.reroute_signals)

