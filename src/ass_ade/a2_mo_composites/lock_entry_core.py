"""Tier a2 — assimilated class 'LockEntry'

Assimilated from: types.py:239-254
"""

from __future__ import annotations


# --- assimilated symbol ---
class LockEntry:
    """One row in the `bindings.lock` ledger.

    `atom_ref` is the stable citation of the bound atom version. In
    Wave 2 this was the entire entry shape. Wave 2 introduces
    `provenance` as a reserve field for Lane W **T-A+5** (SLSA-style
    per-entry provenance records); Wave-2 writers leave it as an empty
    list, Lane W's additive populator fills it with `{repo, commit, path,
    attestation_ref}` rows without a schema bump.

    Lock files remain byte-identical for the same inputs: empty
    `provenance` always serializes as `[]`, never omitted.
    """

    atom_ref: AtomRef
    provenance: list[dict] = field(default_factory=list)

