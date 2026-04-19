# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:518
# Component id: mo.source.ass_ade.identity_verify
from __future__ import annotations

__version__ = "0.1.0"

def identity_verify(self, actor: str | None = None, *, agent_id: str | None = None, **kwargs: Any) -> IdentityVerification:
    """/v1/identity/verify — topology-grounded identity proof. $0.080/request"""
    return self._post_model("/v1/identity/verify", IdentityVerification, {"actor": actor or agent_id or "", **kwargs})
