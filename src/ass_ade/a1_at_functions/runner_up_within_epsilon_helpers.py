"""Tier a1 — assimilated function 'runner_up_within_epsilon'

Assimilated from: scoring.py:451-461
"""

from __future__ import annotations


# --- assimilated symbol ---
def runner_up_within_epsilon(
    ranked: list[AtomScore], constants: ScoringConstants | None = None
) -> AtomScore | None:
    """Return the runner-up within ``SCORING_EPSILON`` of the winner, or None."""
    if len(ranked) < 2:
        return None
    constants = constants or load_constants()
    gap = ranked[0].score - ranked[1].score
    if gap <= constants.SCORING_EPSILON:
        return ranked[1]
    return None

