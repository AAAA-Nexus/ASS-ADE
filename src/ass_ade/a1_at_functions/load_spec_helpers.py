"""Tier a1 — assimilated function 'load_spec'

Assimilated from: scoring.py:87-98
"""

from __future__ import annotations


# --- assimilated symbol ---
def load_spec(path: Path | None = None) -> dict:
    """Load the raw scoring spec YAML. Returns an empty dict on miss."""
    target = path or _DEFAULT_SPEC_PATH
    if not target.exists():
        return {}
    with target.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ScoringWeightsError(
            f"scoring spec at {target} did not parse to a mapping"
        )
    return data

