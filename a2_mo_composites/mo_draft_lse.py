# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_engineorchestrator.py:186
# Component id: mo.source.ass_ade.lse
__version__ = "0.1.0"

    def lse(self):
        if self._lse is None:
            from ass_ade.agent.lse import LSEEngine
            self._lse = LSEEngine(self._config, self._nexus)
        return self._lse
