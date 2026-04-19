# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1101
# Component id: mo.source.a2_mo_composites.vanguard_redteam
from __future__ import annotations

__version__ = "0.1.0"

def vanguard_redteam(self, agent_id: str, target: str, **kwargs: Any) -> VanguardRedTeamResult:
    """POST /v1/vanguard/continuous-redteam — orchestrated red-team audit. $0.100/run"""
    return self._post_model("/v1/vanguard/continuous-redteam", VanguardRedTeamResult, {"agent_id": agent_id, "target": target, **kwargs})
