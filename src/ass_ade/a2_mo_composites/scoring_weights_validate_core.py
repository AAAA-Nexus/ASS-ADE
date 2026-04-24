"""Tier a2 — assimilated method 'ScoringWeights.validate'

Assimilated from: types.py:176-181
"""

from __future__ import annotations


# --- assimilated symbol ---
def validate(self) -> None:
    total = self.sum()
    if abs(total - 1.0) > 1e-6:
        raise ScoringWeightsError(
            f"weights must sum to 1.0 (±1e-6); got {total!r}"
        )

