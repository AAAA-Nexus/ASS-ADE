# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/gates.py:26
# Component id: mo.source.ass_ade.gateresult
__version__ = "0.1.0"

class GateResult:
    """Structured result from a quality gate."""

    gate: str
    passed: bool
    confidence: float = 0.0
    details: dict[str, Any] | None = None
