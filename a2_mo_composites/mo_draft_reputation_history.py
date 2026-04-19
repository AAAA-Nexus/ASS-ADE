# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:571
# Component id: mo.source.ass_ade.reputation_history
__version__ = "0.1.0"

    def reputation_history(self, agent_id: str) -> ReputationHistory:
        """/v1/reputation/history/{id} — exponential-decay weighted history. $0.012/call"""
        return self._get_model(f"/v1/reputation/history/{_pseg(agent_id, 'agent_id')}", ReputationHistory)
