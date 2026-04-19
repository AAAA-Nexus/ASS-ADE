# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_engineorchestrator.py:202
# Component id: mo.source.ass_ade.cie
__version__ = "0.1.0"

    def cie(self):
        if self._cie is None:
            from ass_ade.agent.cie import CIEPipeline
            self._cie = CIEPipeline(self._config, self._nexus)
        return self._cie
