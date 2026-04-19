# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_zero_trust_auth.py:7
# Component id: at.source.a1_at_functions.zero_trust_auth
from __future__ import annotations

__version__ = "0.1.0"

def zero_trust_auth(self, agent_id: int, endpoint: str, capability: str, trust: float = 0.9984, **kwargs: Any) -> ZeroTrustResult:
    """/v1/auth/zero-trust — zero-trust auth primitive. agent_id must be a multiple of G_18 (324). $0.020/call"""
    return self._post_model("/v1/auth/zero-trust", ZeroTrustResult, {
        "agent_id": agent_id, "endpoint": endpoint, "capability": capability, "trust": trust, **kwargs,
    })
