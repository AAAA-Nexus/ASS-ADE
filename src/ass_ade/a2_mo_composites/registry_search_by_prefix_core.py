"""Tier a2 — assimilated method 'Registry.search_by_prefix'

Assimilated from: registry.py:390-398
"""

from __future__ import annotations


# --- assimilated symbol ---
def search_by_prefix(self, domain_prefix: str) -> list[Atom]:
    """Return atoms whose ``canonical_name`` starts with ``domain_prefix``."""
    with self._lock:
        return [
            row.atom
            for row in self._rows.values()
            if not row.deprecated
            and row.atom.canonical_name.startswith(domain_prefix)
        ]

