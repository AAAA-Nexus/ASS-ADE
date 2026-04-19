# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_engineorchestrator.py:151
# Component id: mo.source.a2_mo_composites.lifr
from __future__ import annotations

__version__ = "0.1.0"

def lifr(self):
    if self._lifr is None:
        from ass_ade.agent.lifr_graph import LIFRGraph
        cfg = dict(self._config)
        cfg.setdefault("working_dir", self._working_dir)
        self._lifr = LIFRGraph(cfg, self._nexus)
    return self._lifr
