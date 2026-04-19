# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/orchestrator.py:129
# Component id: sy.source.ass_ade.atlas
__version__ = "0.1.0"

    def atlas(self):
        if self._atlas is None:
            from ass_ade.agent.atlas import Atlas
            self._atlas = Atlas(self._config, self._nexus)
        return self._atlas
