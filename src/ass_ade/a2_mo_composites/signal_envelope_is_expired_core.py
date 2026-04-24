"""Tier a2 — assimilated method 'SignalEnvelope.is_expired'

Assimilated from: types.py:77-81
"""

from __future__ import annotations


# --- assimilated symbol ---
def is_expired(self, now_rfc3339: str) -> bool:
    """Pure: compare RFC-3339 strings lexicographically (UTC only)."""
    if not self.expires_at:
        return False
    return now_rfc3339 >= self.expires_at

