# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:1019
# Component id: mo.source.ass_ade.vanguardsessionresult
from __future__ import annotations

__version__ = "0.1.0"

class VanguardSessionResult(NexusModel):
    """POST /v1/vanguard/wallet/govern-session"""
    session_id: str | None = None
    governed: bool | None = None
    ucan_token: str | None = None
    expires_at: int | None = None
