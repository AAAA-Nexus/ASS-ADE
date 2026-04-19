# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_engineorchestrator.py:149
# Component id: mo.source.ass_ade.lifr
__version__ = "0.1.0"

    def lifr(self):
        if self._lifr is None:
            from ass_ade.agent.lifr_graph import LIFRGraph
            cfg = dict(self._config)
            cfg.setdefault("working_dir", self._working_dir)
            self._lifr = LIFRGraph(cfg, self._nexus)
        return self._lifr
