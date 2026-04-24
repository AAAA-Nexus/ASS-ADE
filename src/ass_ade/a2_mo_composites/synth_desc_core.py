"""Tier a2 — assimilated class 'SynthDesc'

Assimilated from: types.py:222-235
"""

from __future__ import annotations


# --- assimilated symbol ---
class SynthDesc:
    """Instruction set for a SYNTHESIZE outcome.

    Contains only the pre-synthesis context: what the binder knew at
    the point it decided no candidate fit. Post-synthesis the resulting
    Atom lands in the registry via `registry.register`.
    """

    canonical_name: str
    blueprint_signature: str
    rationale: str
    seed_candidates: list[AtomRef] = field(default_factory=list)
    tier: Tier = "a1"
    blueprint_idx: int = 0

