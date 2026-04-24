"""Tier a2 — assimilated class 'ScoringWeights'

Assimilated from: types.py:146-192
"""

from __future__ import annotations


# --- assimilated symbol ---
class ScoringWeights:
    """Weights for `scoring.score`. Must sum to 1.0 (±1e-6).

    Loader enforces the sum invariant. Per-blueprint overrides may
    substitute a different `ScoringWeights` instance; the scorer does
    not mutate the one it was handed.

    Defaults mirror `.ass-ade/specs/scoring-weights.yaml`:
    trust=.25, tests=.20, fit=.15, usage=.10, perf=.10, provenance=.10, recency=.10.
    """

    trust: float = 0.25
    tests: float = 0.20
    fit: float = 0.15
    usage: float = 0.10
    perf: float = 0.10
    provenance: float = 0.10
    recency: float = 0.10

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

    def validate(self) -> None:
        total = self.sum()
        if abs(total - 1.0) > 1e-6:
            raise ScoringWeightsError(
                f"weights must sum to 1.0 (±1e-6); got {total!r}"
            )

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

