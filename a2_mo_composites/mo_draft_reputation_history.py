# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:376
# Component id: mo.source.a2_mo_composites.reputation_history
from __future__ import annotations

__version__ = "0.1.0"

def reputation_history(self, agent_id: str) -> ReputationHistory:
    """/v1/reputation/history/{id} — exponential-decay weighted history. $0.012/call"""
    return self._get_model(f"/v1/reputation/history/{_pseg(agent_id, 'agent_id')}", ReputationHistory)
