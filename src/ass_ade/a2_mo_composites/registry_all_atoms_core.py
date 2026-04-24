"""Tier a2 — assimilated method 'Registry.all_atoms'

Assimilated from: registry.py:578-585
"""

from __future__ import annotations


# --- assimilated symbol ---
def all_atoms(self) -> list[tuple[Atom, AtomMetadata]]:
    """Enumerate all non-deprecated atoms + metadata. Mostly for tests."""
    with self._lock:
        return [
            (row.atom, row.metadata)
            for row in self._rows.values()
            if not row.deprecated
        ]

