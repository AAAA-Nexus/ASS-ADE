# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_validate_acyclic.py:7
# Component id: at.source.a1_at_functions.validate_acyclic
from __future__ import annotations

__version__ = "0.1.0"

def validate_acyclic(plan: dict[str, Any]) -> bool:
    """Return True iff the plan's ``made_of`` graph contains no cycles."""
    return detect_cycles(plan)["acyclic"]
