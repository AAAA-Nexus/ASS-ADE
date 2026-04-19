# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/alphaverus.py:47
# Component id: mo.source.ass_ade.verifiedcode
__version__ = "0.1.0"

class VerifiedCode:
    code: str
    verified: bool
    score: float
    trace: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
