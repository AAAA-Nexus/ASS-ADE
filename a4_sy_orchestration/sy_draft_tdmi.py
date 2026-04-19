# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/orchestrator.py:209
# Component id: sy.source.ass_ade.tdmi
__version__ = "0.1.0"

    def tdmi(self):
        if self._tdmi is None:
            from ass_ade.agent.tdmi import TDMI
            self._tdmi = TDMI(self._config, self._nexus)
        return self._tdmi
