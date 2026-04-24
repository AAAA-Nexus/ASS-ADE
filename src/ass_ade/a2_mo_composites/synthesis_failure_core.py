"""Tier a2 — assimilated class 'SynthesisFailure'

Assimilated from: rebuild/synthesis.py:46-47
"""

from __future__ import annotations


# --- assimilated symbol ---
class SynthesisFailure(RuntimeError):
    """Raised when strict no-stubs synthesis cannot produce a clean body."""

