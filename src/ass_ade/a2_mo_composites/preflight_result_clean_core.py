"""Tier a2 — assimilated method 'PreflightResult.clean'

Assimilated from: nexus.py:136-137
"""

from __future__ import annotations


# --- assimilated symbol ---
def clean(self) -> bool:
    return self.aegis_verdict == "clean" and self.drift_verdict == "fresh"

