# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1055
# Component id: mo.source.a2_mo_composites.design_blueprint
from __future__ import annotations

__version__ = "0.1.0"

def design_blueprint(
    self,
    description: str,
    context: dict[str, Any] | None = None,
    agent_id: str | None = None,
) -> DesignBlueprint:
    """Generate an AAAA-SPEC-004 blueprint from a natural language description."""
    payload: dict[str, Any] = {"description": description}
    if context:
        payload["context"] = context
    if agent_id:
        payload["agent_id"] = agent_id
    return self._post_model("/v1/uep/design", DesignBlueprint, payload)
