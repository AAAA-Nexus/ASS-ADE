# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:913
# Component id: mo.source.ass_ade.trust_score
__version__ = "0.1.0"

    def trust_score(self, agent_id: str, **kwargs: Any) -> TrustScore:
        """/v1/trust/score — TCM-100 formally bounded score in [0,1]. $0.040/query"""
        return self._post_model("/v1/trust/score", TrustScore, {"agent_id": agent_id, **kwargs})
