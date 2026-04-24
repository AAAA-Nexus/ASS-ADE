"""Tier a2 — assimilated method 'ScoringWeights.sum'

Assimilated from: types.py:165-174
"""

from __future__ import annotations


# --- assimilated symbol ---
def sum(self) -> float:
    return (
        self.trust
        + self.tests
        + self.fit
        + self.usage
        + self.perf
        + self.provenance
        + self.recency
    )

