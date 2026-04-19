# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/orchestrator.py:200
# Component id: sy.source.ass_ade.gvu
__version__ = "0.1.0"

    def gvu(self):
        if self._gvu is None:
            from ass_ade.agent.gvu import GVU
            cfg = dict(self._config)
            cfg.setdefault("gvu_state_path", f"{self._working_dir}/.ass-ade/state/gvu.json")
            self._gvu = GVU(cfg, self._nexus)
        return self._gvu
