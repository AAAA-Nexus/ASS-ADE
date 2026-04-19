# Extracted from C:/!ass-ade/src/ass_ade/agent/orchestrator.py:225
# Component id: sy.source.ass_ade.lifr
from __future__ import annotations

__version__ = "0.1.0"

def lifr(self):
    if self._lifr is None:
        from ass_ade.agent.lifr_graph import LIFRGraph
        cfg = dict(self._config)
        cfg.setdefault("working_dir", self._working_dir)
        self._lifr = LIFRGraph(cfg, self._nexus)
    return self._lifr
