"""Tier a2 — assimilated method 'FileSignalBus._ensure_layout'

Assimilated from: bus.py:81-84
"""

from __future__ import annotations


# --- assimilated symbol ---
def _ensure_layout(self) -> None:
    (self.root / "inbox").mkdir(parents=True, exist_ok=True)
    (self.root / "read").mkdir(parents=True, exist_ok=True)
    (self.root / "acks").mkdir(parents=True, exist_ok=True)

