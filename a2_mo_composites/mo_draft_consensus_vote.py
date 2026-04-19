# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:857
# Component id: mo.source.ass_ade.consensus_vote
__version__ = "0.1.0"

    def consensus_vote(self, session_id: str, agent_id: str, output_hash: str, confidence: float, **kwargs: Any) -> dict:
        """/v1/consensus/session/{id}/vote — cast consensus vote. $0.020/call"""
        return self._post_raw(f"/v1/consensus/session/{_pseg(session_id, 'session_id')}/vote", {
            "agent_id": agent_id, "output_hash": output_hash, "confidence": confidence, **kwargs,
        })
