# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:380
# Component id: mo.source.a2_mo_composites.reputation_record
from __future__ import annotations

__version__ = "0.1.0"

def reputation_record(self, agent_id: str, success: bool = True, quality: float = 1.0, latency_ms: float = 0.0, **kwargs: Any) -> ReputationRecord:
    """/v1/reputation/record — append a reputation event. $0.008/call"""
    return self._post_model("/v1/reputation/record", ReputationRecord, {
        "agent_id": agent_id, "success": success, "quality": quality, "latency_ms": latency_ms, **kwargs,
    })
