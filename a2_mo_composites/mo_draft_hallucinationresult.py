# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:130
# Component id: mo.source.ass_ade.hallucinationresult
__version__ = "0.1.0"

class HallucinationResult(NexusModel):
    """/v1/oracle/hallucination"""
    policy_epsilon: float | None = None
    verdict: str | None = None       # "safe" | "caution" | "unsafe"
    ceiling: str | None = None       # "proved-not-estimated"
    confidence: float | None = None
