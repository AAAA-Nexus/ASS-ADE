# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:730
# Component id: mo.source.ass_ade.agent_quarantine
from __future__ import annotations

__version__ = "0.1.0"

def agent_quarantine(self, agent_id: str, reason: str, **kwargs: Any) -> QuarantineResult:
    """/v1/agent/quarantine — isolate non-compliant agents (SEC-309). $0.040/request"""
    return self._post_model("/v1/agent/quarantine", QuarantineResult, {"agent_id": agent_id, "reason": reason, **kwargs})
