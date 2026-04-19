# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/orchestrator.py:262
# Component id: sy.source.ass_ade.lse
__version__ = "0.1.0"

    def lse(self):
        if self._lse is None:
            from ass_ade.agent.lse import LSEEngine
            self._lse = LSEEngine(self._config, self._nexus)
        return self._lse
