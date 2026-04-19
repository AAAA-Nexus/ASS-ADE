# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_tier_for_complexity.py:7
# Component id: at.source.a1_at_functions.tier_for_complexity
from __future__ import annotations

__version__ = "0.1.0"

def tier_for_complexity(complexity: float) -> ModelTier:
    """Map a complexity score to a model tier."""
    if complexity < 0.3:
        return ModelTier.FAST
    elif complexity < 0.6:
        return ModelTier.STANDARD
    else:
        return ModelTier.DEEP
