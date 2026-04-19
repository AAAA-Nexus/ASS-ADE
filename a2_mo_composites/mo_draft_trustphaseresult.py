# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:138
# Component id: mo.source.ass_ade.trustphaseresult
__version__ = "0.1.0"

class TrustPhaseResult(NexusModel):
    """/v1/oracle/v-ai — V_AI phase oracle"""
    phase: float | None = None
    certified: bool | None = None
    monotonicity_preserved: bool | None = None
