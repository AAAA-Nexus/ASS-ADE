# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1217
# Component id: mo.source.ass_ade.docs_generate
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
