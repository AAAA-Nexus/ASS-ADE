# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_compliance_oversight.py:7
# Component id: at.source.a1_at_functions.compliance_oversight
from __future__ import annotations

__version__ = "0.1.0"

def compliance_oversight(self, reviewer: str, decision: str, **kwargs: Any) -> OversightEvent:
    """/v1/compliance/oversight — HITL review attestation (OVS-100). $0.020/event"""
    return self._post_model("/v1/compliance/oversight", OversightEvent, {"reviewer": reviewer, "decision": decision, **kwargs})
