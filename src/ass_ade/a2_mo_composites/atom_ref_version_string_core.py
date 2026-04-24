"""Tier a2 — assimilated method 'AtomRef.version_string'

Assimilated from: types.py:73-74
"""

from __future__ import annotations


# --- assimilated symbol ---
def version_string(self) -> str:
    return f"{self.version_major}.{self.version_minor}.{self.version_patch}"

