# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_epistemicrouteresult.py:7
# Component id: sy.source.a4_sy_orchestration.epistemicrouteresult
from __future__ import annotations

__version__ = "0.1.0"

class EpistemicRouteResult(NexusModel):
    """/v1/aegis/router/epistemic-bound"""
    routed_to: str | None = None
    epsilon_bound: float | None = None
    rationale: str | None = None
