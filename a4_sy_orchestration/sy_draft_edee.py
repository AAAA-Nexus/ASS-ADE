# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/orchestrator.py:216
# Component id: sy.source.ass_ade.edee
__version__ = "0.1.0"

    def edee(self):
        if self._edee is None:
            from ass_ade.agent.edee import EDEE
            cfg = dict(self._config)
            cfg.setdefault("working_dir", self._working_dir)
            self._edee = EDEE(cfg, self._nexus)
        return self._edee
