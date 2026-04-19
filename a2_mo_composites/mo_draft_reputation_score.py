# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:372
# Component id: mo.source.a2_mo_composites.reputation_score
from __future__ import annotations

__version__ = "0.1.0"

def reputation_score(self, agent_id: str) -> ReputationScore:
    """/v1/reputation/score/{id} — tier + fee multiplier. $0.008/call"""
    return self._get_model(f"/v1/reputation/score/{_pseg(agent_id, 'agent_id')}", ReputationScore)
