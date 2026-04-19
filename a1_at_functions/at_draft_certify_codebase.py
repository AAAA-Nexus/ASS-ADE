# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_certify_codebase.py:7
# Component id: at.source.a1_at_functions.certify_codebase
from __future__ import annotations

__version__ = "0.1.0"

def certify_codebase(
    self,
    local_certificate: dict[str, Any],
    agent_id: str | None = None,
) -> CertifyResult:
    """Sign and certify a codebase via AAAA-Nexus PQC signing."""
    payload: dict[str, Any] = {"certificate": local_certificate}
    if agent_id:
        payload["agent_id"] = agent_id
    return self._post_model("/v1/certify/codebase", CertifyResult, payload)
