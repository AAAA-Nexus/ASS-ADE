# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_tca.py:7
# Component id: at.source.a1_at_functions.tca
from __future__ import annotations

__version__ = "0.1.0"

def tca(self):
    if self._tca is None:
        from ass_ade.agent.tca import TCAEngine
        cfg = dict(self._config)
        cfg.setdefault("working_dir", self._working_dir)
        self._tca = TCAEngine(cfg, self._nexus)
    return self._tca
