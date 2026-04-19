# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_trust_decay.py:7
# Component id: at.source.a1_at_functions.trust_decay
from __future__ import annotations

__version__ = "0.1.0"

def trust_decay(self, agent_id: str, epochs: int, **kwargs: Any) -> TrustDecayResult:
    """/v1/trust/decay — P2P trust decay oracle. $0.008/call"""
    return self._post_model("/v1/trust/decay", TrustDecayResult, {"agent_id": agent_id, "epochs": epochs, **kwargs})
