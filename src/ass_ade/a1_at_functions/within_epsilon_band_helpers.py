"""Tier a1 — assimilated function 'within_epsilon_band'

Assimilated from: scoring.py:464-472
"""

from __future__ import annotations


# --- assimilated symbol ---
def within_epsilon_band(
    ranked: list[AtomScore], constants: ScoringConstants | None = None
) -> list[AtomScore]:
    """Return every tail entry within SCORING_EPSILON of the winner."""
    if not ranked:
        return []
    constants = constants or load_constants()
    cutoff = ranked[0].score - constants.SCORING_EPSILON
    return [s for s in ranked[1:] if s.score >= cutoff]

