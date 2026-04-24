"""Tier a2 — assimilated method 'FileSignalBus.log_path'

Assimilated from: bus.py:91-92
"""

from __future__ import annotations


# --- assimilated symbol ---
def log_path(self) -> Path:
    return self.root / "broadcast.log.jsonl"

