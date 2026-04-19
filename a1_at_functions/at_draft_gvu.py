# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_gvu.py:7
# Component id: at.source.a1_at_functions.gvu
from __future__ import annotations

__version__ = "0.1.0"

def gvu(self):
    if self._gvu is None:
        from ass_ade.agent.gvu import GVU
        cfg = dict(self._config)
        cfg.setdefault("gvu_state_path", f"{self._working_dir}/.ass-ade/state/gvu.json")
        self._gvu = GVU(cfg, self._nexus)
    return self._gvu
