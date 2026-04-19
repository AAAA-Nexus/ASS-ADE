# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_engineorchestrator.py:193
# Component id: mo.source.ass_ade.tca
__version__ = "0.1.0"

    def tca(self):
        if self._tca is None:
            from ass_ade.agent.tca import TCAEngine
            cfg = dict(self._config)
            cfg.setdefault("working_dir", self._working_dir)
            self._tca = TCAEngine(cfg, self._nexus)
        return self._tca
