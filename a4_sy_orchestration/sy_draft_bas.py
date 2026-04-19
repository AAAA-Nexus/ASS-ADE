# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/orchestrator.py:136
# Component id: sy.source.ass_ade.bas
__version__ = "0.1.0"

    def bas(self):
        if self._bas is None:
            from ass_ade.agent.bas import BAS
            self._bas = BAS(self._config, self._nexus)
        return self._bas
