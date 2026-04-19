# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:521
# Component id: sy.source.ass_ade.epistemicrouteresult
from __future__ import annotations

__version__ = "0.1.0"

class EpistemicRouteResult(NexusModel):
    """/v1/aegis/router/epistemic-bound"""
    routed_to: str | None = None
    epsilon_bound: float | None = None
    rationale: str | None = None
