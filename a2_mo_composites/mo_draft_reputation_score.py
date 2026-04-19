# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:567
# Component id: mo.source.ass_ade.reputation_score
__version__ = "0.1.0"

    def reputation_score(self, agent_id: str) -> ReputationScore:
        """/v1/reputation/score/{id} — tier + fee multiplier. $0.008/call"""
        return self._get_model(f"/v1/reputation/score/{_pseg(agent_id, 'agent_id')}", ReputationScore)
