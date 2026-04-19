# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_trustverificationgate.py:37
# Component id: at.source.ass_ade.get_trust_score
__version__ = "0.1.0"

    def get_trust_score(self, agent_id: str) -> float:
        if agent_id in self._scores:
            return self._scores[agent_id]
        if self._nexus is not None and hasattr(self._nexus, "trust_score"):
            try:
                r = self._nexus.trust_score(agent_id)
                score = float(getattr(r, "score", 0.5))
                self._scores[agent_id] = score
                return score
            except Exception:
                pass
        return 0.5
