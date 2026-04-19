# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1113
# Component id: mo.source.a2_mo_composites.vanguard_start_session
from __future__ import annotations

__version__ = "0.1.0"

def vanguard_start_session(self, agent_id: str, **kwargs: Any) -> VanguardSessionResult:
    """POST /v1/vanguard/session/start — start a VANGUARD wallet session. $0.040/call"""
    return self._post_model("/v1/vanguard/session/start", VanguardSessionResult, {"agent_id": agent_id, **kwargs})
