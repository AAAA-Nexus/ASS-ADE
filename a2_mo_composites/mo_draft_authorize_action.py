# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:581
# Component id: mo.source.a2_mo_composites.authorize_action
from __future__ import annotations

__version__ = "0.1.0"

def authorize_action(self, agent_id: str, action: str, delegation_depth: int = 0, **kwargs: Any) -> AuthorizeActionResult:
    """/v1/authorize/action — pre-action authorization gateway (OAP-100). $0.040/call"""
    return self._post_model("/v1/authorize/action", AuthorizeActionResult, {
        "agent_id": agent_id, "action": action, "delegation_depth": delegation_depth, **kwargs,
    })
