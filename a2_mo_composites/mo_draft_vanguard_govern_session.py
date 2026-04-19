# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1109
# Component id: mo.source.a2_mo_composites.vanguard_govern_session
from __future__ import annotations

__version__ = "0.1.0"

def vanguard_govern_session(self, agent_id: str, session_key: str | None = None, *, wallet: str | None = None, **kwargs: Any) -> VanguardSessionResult:
    """POST /v1/vanguard/wallet/govern-session — UCAN wallet session control. $0.040/call"""
    return self._post_model("/v1/vanguard/wallet/govern-session", VanguardSessionResult, {"agent_id": agent_id, "session_key": session_key or wallet or "", **kwargs})
