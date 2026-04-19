# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/orchestrator.py:255
# Component id: sy.source.ass_ade.severa
__version__ = "0.1.0"

    def severa(self):
        if self._severa is None:
            from ass_ade.agent.severa import Severa
            self._severa = Severa(self._config, self._nexus)
        return self._severa
