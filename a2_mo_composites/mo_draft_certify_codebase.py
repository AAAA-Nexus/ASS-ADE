# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1044
# Component id: mo.source.a2_mo_composites.certify_codebase
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
