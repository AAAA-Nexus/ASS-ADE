# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:152
# Component id: mo.source.ass_ade.trustdecayresult
__version__ = "0.1.0"

class TrustDecayResult(NexusModel):
    """/v1/trust/decay"""
    decayed_score: float | None = None
    original_score: float | None = None
    epochs_elapsed: int | None = None
