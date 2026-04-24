"""Tier a1 — assimilated function 'load_weights'

Assimilated from: scoring.py:101-115
"""

from __future__ import annotations


# --- assimilated symbol ---
def load_weights(path: Path | None = None) -> ScoringWeights:
    """Load default weights. Raises if the sum is off by >1e-6."""
    spec = load_spec(path)
    w = spec.get("weights", {}) or {}
    weights = ScoringWeights(
        trust=float(w.get("trust", 0.25)),
        tests=float(w.get("tests", 0.20)),
        fit=float(w.get("fit", 0.15)),
        usage=float(w.get("usage", 0.10)),
        perf=float(w.get("perf", 0.10)),
        provenance=float(w.get("provenance", 0.10)),
        recency=float(w.get("recency", 0.10)),
    )
    weights.validate()
    return weights

