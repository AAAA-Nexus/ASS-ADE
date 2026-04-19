# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_epistemicrouteresult.py:5
# Component id: sy.source.ass_ade.epistemicrouteresult
__version__ = "0.1.0"

class EpistemicRouteResult(NexusModel):
    """/v1/aegis/router/epistemic-bound"""
    routed_to: str | None = None
    epsilon_bound: float | None = None
    rationale: str | None = None
