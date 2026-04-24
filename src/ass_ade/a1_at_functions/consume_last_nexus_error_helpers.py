"""Tier a1 — assimilated function 'consume_last_nexus_error'

Assimilated from: rebuild/synthesis.py:60-65
"""

from __future__ import annotations


# --- assimilated symbol ---
def consume_last_nexus_error() -> str | None:
    """Return and clear the most recent Nexus failure. Used by orchestrators."""
    global _LAST_NEXUS_ERROR
    msg = _LAST_NEXUS_ERROR
    _LAST_NEXUS_ERROR = None
    return msg

