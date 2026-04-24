"""Tier a2 — assimilated class 'ScoringConstants'

Assimilated from: scoring.py:78-84
"""

from __future__ import annotations


# --- assimilated symbol ---
class ScoringConstants:
    """Public scoring constants from ``scoring-weights.yaml``."""

    SCORING_EPSILON: float = 0.02
    PUBLIC_RECENCY_HALF_LIFE_DAYS: float = 180.0
    TRUST_CEILING_UNTESTED_FACTOR: float = 0.85
    MIN_CANDIDATE_SCORE_FLOOR: float = 0.0

