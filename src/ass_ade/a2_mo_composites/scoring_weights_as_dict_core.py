"""Tier a2 — assimilated method 'ScoringWeights.as_dict'

Assimilated from: types.py:183-192
"""

from __future__ import annotations


# --- assimilated symbol ---
def as_dict(self) -> dict[str, float]:
    return {
        "trust": self.trust,
        "tests": self.tests,
        "fit": self.fit,
        "usage": self.usage,
        "perf": self.perf,
        "provenance": self.provenance,
        "recency": self.recency,
    }

