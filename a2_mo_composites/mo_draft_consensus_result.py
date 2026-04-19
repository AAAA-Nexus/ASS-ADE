# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:863
# Component id: mo.source.ass_ade.consensus_result
__version__ = "0.1.0"

    def consensus_result(self, session_id: str) -> ConsensusResult:
        """/v1/consensus/session/{id}/result — certified winning output. $0.020/call"""
        return self._get_model(f"/v1/consensus/session/{_pseg(session_id, 'session_id')}/result", ConsensusResult)
