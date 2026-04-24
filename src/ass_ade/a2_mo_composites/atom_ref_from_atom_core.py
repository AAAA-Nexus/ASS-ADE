"""Tier a2 — assimilated method 'AtomRef.from_atom'

Assimilated from: types.py:77-84
"""

from __future__ import annotations


# --- assimilated symbol ---
def from_atom(cls, atom: Atom) -> AtomRef:
    return cls(
        canonical_name=atom.canonical_name,
        version_major=atom.version_major,
        version_minor=atom.version_minor,
        version_patch=atom.version_patch,
        sig_fp=atom.sig_fp,
    )

