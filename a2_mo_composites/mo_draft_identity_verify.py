# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:323
# Component id: mo.source.a2_mo_composites.identity_verify
from __future__ import annotations

__version__ = "0.1.0"

def identity_verify(self, actor: str | None = None, *, agent_id: str | None = None, **kwargs: Any) -> IdentityVerification:
    """/v1/identity/verify — topology-grounded identity proof. $0.080/request"""
    return self._post_model("/v1/identity/verify", IdentityVerification, {"actor": actor or agent_id or "", **kwargs})
