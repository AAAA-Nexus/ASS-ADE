"""Tier a1 — assimilated function 'search_by_sig_fp'

Assimilated from: registry.py:795-797
"""

from __future__ import annotations


# --- assimilated symbol ---
def search_by_sig_fp(sig_fp_hex: str, within: float | None = None) -> list[Atom]:
    """Module-level convenience wrapper over :meth:`Registry.search_by_sig_fp`."""
    return default_registry().search_by_sig_fp(sig_fp_hex, within=within)

