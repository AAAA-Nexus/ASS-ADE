# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/orchestrator.py:278
# Component id: sy.source.ass_ade.cie
__version__ = "0.1.0"

    def cie(self):
        if self._cie is None:
            from ass_ade.agent.cie import CIEPipeline
            self._cie = CIEPipeline(self._config, self._nexus)
        return self._cie
