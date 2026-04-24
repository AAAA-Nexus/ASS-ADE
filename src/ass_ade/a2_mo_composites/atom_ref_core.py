"""Tier a2 — assimilated class 'AtomRef'

Assimilated from: types.py:60-84
"""

from __future__ import annotations


# --- assimilated symbol ---
class AtomRef:
    """Stable reference to a specific Atom version in the registry.

    Used anywhere we need to cite an Atom without embedding its full body
    (bindings.lock, genesis events, score breakdowns, etc.).
    """

    canonical_name: str
    version_major: int
    version_minor: int
    version_patch: int
    sig_fp: str

    def version_string(self) -> str:
        return f"{self.version_major}.{self.version_minor}.{self.version_patch}"

    @classmethod
    def from_atom(cls, atom: Atom) -> AtomRef:
        return cls(
            canonical_name=atom.canonical_name,
            version_major=atom.version_major,
            version_minor=atom.version_minor,
            version_patch=atom.version_patch,
            sig_fp=atom.sig_fp,
        )

