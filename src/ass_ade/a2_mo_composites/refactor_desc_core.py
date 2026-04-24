"""Tier a2 — assimilated class 'RefactorDesc'

Assimilated from: types.py:212-218
"""

from __future__ import annotations


# --- assimilated symbol ---
class RefactorDesc:
    """Instruction set for a REFACTOR outcome."""

    target_ref: AtomRef
    near_candidates: list[AtomRef]
    rationale: str
    blueprint_idx: int = 0

