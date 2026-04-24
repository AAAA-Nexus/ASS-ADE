"""Tier a2 — assimilated method 'Registry.iter_atoms'

Assimilated from: registry.py:545-568
"""

from __future__ import annotations


# --- assimilated symbol ---
def iter_atoms(self, *, filter=None):
    """Stream every non-deprecated atom, lazily.

    Per ``handoffs/parent-answers-wave-2.md §5`` this is the
    canonical enumeration API for ``from_nl(..., registry_snapshot=
    iter_atoms())``. The generator is lazy and memory-bounded —
    Wave-4 sharded registries can implement the same contract
    without materializing every atom up-front.

    ``filter`` is an optional callable ``Atom -> bool``. When
    provided, only atoms where ``filter(atom)`` is truthy are
    yielded.

    Returns an iterator rather than a list: callers that need
    indexed access should call :meth:`snapshot` instead.
    """
    # Copy refs under the lock; yield outside so long-running
    # downstream iteration doesn't hold the registry open.
    with self._lock:
        atoms = [row.atom for row in self._rows.values() if not row.deprecated]
    for atom in atoms:
        if filter is not None and not filter(atom):
            continue
        yield atom

