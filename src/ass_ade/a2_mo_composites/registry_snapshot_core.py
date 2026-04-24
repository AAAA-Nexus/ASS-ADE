"""Tier a2 — assimilated method 'Registry.snapshot'

Assimilated from: registry.py:570-576
"""

from __future__ import annotations


# --- assimilated symbol ---
def snapshot(self) -> list[Atom]:
    """Materialize :meth:`iter_atoms` as a list.

    Convenience wrapper for callers that need indexed access or
    multiple passes. Equivalent to ``list(self.iter_atoms())``.
    """
    return list(self.iter_atoms())

