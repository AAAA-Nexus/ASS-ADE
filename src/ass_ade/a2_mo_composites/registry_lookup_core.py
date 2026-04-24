"""Tier a2 — assimilated method 'Registry.lookup'

Assimilated from: registry.py:315-341
"""

from __future__ import annotations


# --- assimilated symbol ---
def lookup(
    self,
    canonical_name: str,
    version_range: str | None = None,
) -> Atom | None:
    """Return the Atom at ``canonical_name`` matching ``version_range``.

    ``version_range`` syntax supports three forms (kept intentionally
    small for v1; extend via ADR addendum):

    * ``None`` — any version matches.
    * ``"1.2.3"`` — exact version match.
    * ``"^1.2"`` — caret range: same major, minor ``>=`` pinned
      minor; patch unconstrained.

    Returns ``None`` if no atom matches, the atom is deprecated, or
    the version range filters it out.
    """
    with self._lock:
        row = self._rows.get(canonical_name)
        if row is None or row.deprecated:
            return None
        if version_range is None:
            return row.atom
        if not _version_matches(row.atom, version_range):
            return None
        return row.atom

