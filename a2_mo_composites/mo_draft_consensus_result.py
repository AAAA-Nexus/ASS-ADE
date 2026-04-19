# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:668
# Component id: mo.source.a2_mo_composites.consensus_result
from __future__ import annotations

__version__ = "0.1.0"

def consensus_result(self, session_id: str) -> ConsensusResult:
    """/v1/consensus/session/{id}/result — certified winning output. $0.020/call"""
    return self._get_model(f"/v1/consensus/session/{_pseg(session_id, 'session_id')}/result", ConsensusResult)
