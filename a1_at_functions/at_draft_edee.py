# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_edee.py:7
# Component id: at.source.a1_at_functions.edee
from __future__ import annotations

__version__ = "0.1.0"

def edee(self):
    if self._edee is None:
        from ass_ade.agent.edee import EDEE
        cfg = dict(self._config)
        cfg.setdefault("working_dir", self._working_dir)
        self._edee = EDEE(cfg, self._nexus)
    return self._edee
