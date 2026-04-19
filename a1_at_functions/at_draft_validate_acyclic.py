# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/rebuild/cycle_detector.py:152
# Component id: at.source.ass_ade.validate_acyclic
__version__ = "0.1.0"

def validate_acyclic(plan: dict[str, Any]) -> bool:
    """Return True iff the plan's ``made_of`` graph contains no cycles."""
    return detect_cycles(plan)["acyclic"]
