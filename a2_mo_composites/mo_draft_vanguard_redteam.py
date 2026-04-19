# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1296
# Component id: mo.source.ass_ade.vanguard_redteam
from __future__ import annotations

__version__ = "0.1.0"

def vanguard_redteam(self, agent_id: str, target: str, **kwargs: Any) -> VanguardRedTeamResult:
    """POST /v1/vanguard/continuous-redteam — orchestrated red-team audit. $0.100/run"""
    return self._post_model("/v1/vanguard/continuous-redteam", VanguardRedTeamResult, {"agent_id": agent_id, "target": target, **kwargs})
