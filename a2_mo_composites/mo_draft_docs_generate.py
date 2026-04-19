# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1022
# Component id: mo.source.a2_mo_composites.docs_generate
from __future__ import annotations

__version__ = "0.1.0"

def docs_generate(
    self,
    path_analysis: dict[str, Any],
    agent_id: str | None = None,
) -> DocsResult:
    """Generate documentation suite via AAAA-Nexus synthesis engine."""
    payload: dict[str, Any] = {"path_analysis": path_analysis}
    if agent_id:
        payload["agent_id"] = agent_id
    return self._post_model("/v1/docs/generate", DocsResult, payload)
