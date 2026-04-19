# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_lsedecision.py:5
# Component id: mo.source.ass_ade.lsedecision
__version__ = "0.1.0"

class LSEDecision:
    model: str
    tier: str
    reason: str
    trs_score: float
    complexity: str
    provider: str | None = None  # provider name from catalog (e.g., "groq")
