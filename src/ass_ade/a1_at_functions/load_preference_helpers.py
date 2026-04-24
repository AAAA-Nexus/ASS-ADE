"""Tier a1 — assimilated function 'load_preference'

Assimilated from: scoring.py:146-165
"""

from __future__ import annotations


# --- assimilated symbol ---
def load_preference(name: str, path: Path | None = None) -> ScoringWeights:
    """Return a named preference profile as :class:`ScoringWeights`."""
    spec = load_spec(path)
    profiles = spec.get("preference_profiles", {}) or {}
    if name not in profiles:
        raise ScoringWeightsError(
            f"preference profile {name!r} not declared in scoring spec"
        )
    p = profiles[name]
    weights = ScoringWeights(
        trust=float(p["trust"]),
        tests=float(p["tests"]),
        fit=float(p["fit"]),
        usage=float(p["usage"]),
        perf=float(p["perf"]),
        provenance=float(p["provenance"]),
        recency=float(p["recency"]),
    )
    weights.validate()
    return weights

