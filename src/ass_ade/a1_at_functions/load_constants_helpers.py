"""Tier a1 — assimilated function 'load_constants'

Assimilated from: scoring.py:118-143
"""

from __future__ import annotations


# --- assimilated symbol ---
def load_constants(path: Path | None = None) -> ScoringConstants:
    spec = load_spec(path)
    c = spec.get("constants", {}) or {}
    return ScoringConstants(
        SCORING_EPSILON=float(
            c.get("SCORING_EPSILON", _DEFAULT_CONSTANTS["SCORING_EPSILON"])
        ),
        PUBLIC_RECENCY_HALF_LIFE_DAYS=float(
            c.get(
                "PUBLIC_RECENCY_HALF_LIFE_DAYS",
                _DEFAULT_CONSTANTS["PUBLIC_RECENCY_HALF_LIFE_DAYS"],
            )
        ),
        TRUST_CEILING_UNTESTED_FACTOR=float(
            c.get(
                "TRUST_CEILING_UNTESTED_FACTOR",
                _DEFAULT_CONSTANTS["TRUST_CEILING_UNTESTED_FACTOR"],
            )
        ),
        MIN_CANDIDATE_SCORE_FLOOR=float(
            c.get(
                "MIN_CANDIDATE_SCORE_FLOOR",
                _DEFAULT_CONSTANTS["MIN_CANDIDATE_SCORE_FLOOR"],
            )
        ),
    )

