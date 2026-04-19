# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_forgeverifyresult.py:7
# Component id: mo.source.a2_mo_composites.forgeverifyresult
from __future__ import annotations

__version__ = "0.1.0"

class ForgeVerifyResult(NexusModel):
    """POST /v1/forge/verify"""
    verified: bool | None = None
    agent_id: str | None = None
    score: float | None = None
    badge_awarded: str | None = None
