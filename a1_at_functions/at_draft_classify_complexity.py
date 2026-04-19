# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_classify_complexity.py:5
# Component id: at.source.ass_ade.classify_complexity
__version__ = "0.1.0"

def classify_complexity(message: str) -> float:
    """Estimate task complexity from a user message.

    Returns a score in [0, 1].
    """
    c_code = 0.3 if _CODE_PATTERN.search(message) else 0.0
    c_length = min(0.3, len(message) / 3000)
    c_multi = 0.2 if _MULTI_STEP_PATTERN.search(message) else 0.0
    c_formal = 0.2 if _FORMAL_PATTERN.search(message) else 0.0
    return min(1.0, c_code + c_length + c_multi + c_formal)
