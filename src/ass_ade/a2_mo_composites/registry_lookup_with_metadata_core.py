"""Tier a2 — assimilated method 'Registry.lookup_with_metadata'

Assimilated from: registry.py:343-355
"""

from __future__ import annotations


# --- assimilated symbol ---
def lookup_with_metadata(
    self, canonical_name: str, version_range: str | None = None
) -> tuple[Atom, AtomMetadata] | None:
    """Lookup variant that also returns the scorer-facing metadata."""
    with self._lock:
        row = self._rows.get(canonical_name)
        if row is None or row.deprecated:
            return None
        if version_range is not None and not _version_matches(
            row.atom, version_range
        ):
            return None
        return row.atom, row.metadata

