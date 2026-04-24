"""Tier a1 — assimilated function 'validate_acyclic'

Assimilated from: rebuild/cycle_detector.py:152-154
"""

from __future__ import annotations


# --- assimilated symbol ---
def validate_acyclic(plan: dict[str, Any]) -> bool:
    """Return True iff the plan's ``made_of`` graph contains no cycles."""
    return detect_cycles(plan)["acyclic"]

