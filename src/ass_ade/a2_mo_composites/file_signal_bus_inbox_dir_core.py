"""Tier a2 — assimilated method 'FileSignalBus.inbox_dir'

Assimilated from: bus.py:87-88
"""

from __future__ import annotations


# --- assimilated symbol ---
def inbox_dir(self) -> Path:
    return self.root / "inbox"

