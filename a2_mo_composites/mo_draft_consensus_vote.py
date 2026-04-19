# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:662
# Component id: mo.source.a2_mo_composites.consensus_vote
from __future__ import annotations

__version__ = "0.1.0"

def consensus_vote(self, session_id: str, agent_id: str, output_hash: str, confidence: float, **kwargs: Any) -> dict:
    """/v1/consensus/session/{id}/vote — cast consensus vote. $0.020/call"""
    return self._post_raw(f"/v1/consensus/session/{_pseg(session_id, 'session_id')}/vote", {
        "agent_id": agent_id, "output_hash": output_hash, "confidence": confidence, **kwargs,
    })
