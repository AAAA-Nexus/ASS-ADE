# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/routing.py:109
# Component id: at.source.ass_ade.tier_for_complexity
__version__ = "0.1.0"

def tier_for_complexity(complexity: float) -> ModelTier:
    """Map a complexity score to a model tier."""
    if complexity < 0.3:
        return ModelTier.FAST
    elif complexity < 0.6:
        return ModelTier.STANDARD
    else:
        return ModelTier.DEEP
