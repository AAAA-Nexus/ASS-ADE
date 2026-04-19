# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1072
# Component id: mo.source.ass_ade.compliance_oversight
from __future__ import annotations

__version__ = "0.1.0"

def compliance_oversight(self, reviewer: str, decision: str, **kwargs: Any) -> OversightEvent:
    """/v1/compliance/oversight — HITL review attestation (OVS-100). $0.020/event"""
    return self._post_model("/v1/compliance/oversight", OversightEvent, {"reviewer": reviewer, "decision": decision, **kwargs})
