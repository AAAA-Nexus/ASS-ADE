"""Tier a2 — assimilated class 'AtomScore'

Assimilated from: types.py:196-208
"""

from __future__ import annotations


# --- assimilated symbol ---
class AtomScore:
    """Binder candidate score record.

    Emitted to the public genesis log on every binder decision; this
    event stream is the primary LoRA training signal (ADR-008).
    """

    atom_ref: AtomRef
    score: float
    breakdown: dict[str, float]
    weights: ScoringWeights
    tiebreak_path: list[str] = field(default_factory=list)
    tags: tuple[str, ...] = ()

