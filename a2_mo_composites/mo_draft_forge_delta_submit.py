# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1164
# Component id: mo.source.a2_mo_composites.forge_delta_submit
from __future__ import annotations

__version__ = "0.1.0"

def forge_delta_submit(self, agent_id: str, delta: dict, **kwargs: Any) -> ForgeDeltaSubmitResult:
    """POST /v1/forge/delta/submit — submit improvement delta. Free."""
    return self._post_model("/v1/forge/delta/submit", ForgeDeltaSubmitResult, {"agent_id": agent_id, "delta": delta, **kwargs})
