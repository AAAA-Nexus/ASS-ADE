# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_vanguardsessionresult.py:7
# Component id: mo.source.a2_mo_composites.vanguardsessionresult
from __future__ import annotations

__version__ = "0.1.0"

class VanguardSessionResult(NexusModel):
    """POST /v1/vanguard/wallet/govern-session"""
    session_id: str | None = None
    governed: bool | None = None
    ucan_token: str | None = None
    expires_at: int | None = None
