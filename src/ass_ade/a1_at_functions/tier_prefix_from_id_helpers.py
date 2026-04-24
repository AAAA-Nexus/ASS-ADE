"""Tier a1 — assimilated function 'tier_prefix_from_id'

Assimilated from: rebuild/tier_purity.py:27-32
"""

from __future__ import annotations


# --- assimilated symbol ---
def tier_prefix_from_id(dep_id: str) -> str | None:
    """Return the tier head from a component id like ``a1.parse.foo``."""
    if "." not in dep_id:
        return None
    prefix = dep_id.split(".", 1)[0]
    return prefix if prefix in PREFIX_TO_TIER else None

