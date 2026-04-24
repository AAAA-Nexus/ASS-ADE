"""Tier a1 — assimilated function 'lookup'

Assimilated from: registry.py:783-787
"""

from __future__ import annotations


# --- assimilated symbol ---
def lookup(
    canonical_name: str, version_range: str | None = None
) -> Atom | None:
    """Module-level convenience wrapper over :meth:`Registry.lookup`."""
    return default_registry().lookup(canonical_name, version_range)

