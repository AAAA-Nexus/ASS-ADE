# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:1071
# Component id: mo.source.ass_ade.forgeverifyresult
from __future__ import annotations

__version__ = "0.1.0"

class ForgeVerifyResult(NexusModel):
    """POST /v1/forge/verify"""
    verified: bool | None = None
    agent_id: str | None = None
    score: float | None = None
    badge_awarded: str | None = None
