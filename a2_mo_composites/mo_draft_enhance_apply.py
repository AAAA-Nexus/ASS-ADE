# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1278
# Component id: mo.source.a2_mo_composites.enhance_apply
from __future__ import annotations

__version__ = "0.1.0"

def enhance_apply(
    self,
    improvement_ids: list[int],
    local_report: dict[str, Any],
    agent_id: str | None = None,
) -> EnhanceApplyResult:
    """Apply selected enhancements: generate blueprints and trigger rebuild."""
    payload: dict[str, Any] = {
        "improvement_ids": improvement_ids,
        "local_report": local_report,
    }
    if agent_id:
        payload["agent_id"] = agent_id
    return self._post_model("/v1/enhance/apply", EnhanceApplyResult, payload)
