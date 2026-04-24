"""Tier a2 — assimilated method 'TickResult.must_halt'

Assimilated from: coordinator.py:43-44
"""

from __future__ import annotations


# --- assimilated symbol ---
def must_halt(self) -> bool:
    return bool(self.halt_signals)

