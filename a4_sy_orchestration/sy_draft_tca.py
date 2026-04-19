# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/orchestrator.py:269
# Component id: sy.source.ass_ade.tca
__version__ = "0.1.0"

    def tca(self):
        if self._tca is None:
            from ass_ade.agent.tca import TCAEngine
            cfg = dict(self._config)
            cfg.setdefault("working_dir", self._working_dir)
            self._tca = TCAEngine(cfg, self._nexus)
        return self._tca
