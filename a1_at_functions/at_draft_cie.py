# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_cie.py:7
# Component id: at.source.a1_at_functions.cie
from __future__ import annotations

__version__ = "0.1.0"

def cie(self):
    if self._cie is None:
        from ass_ade.agent.cie import CIEPipeline
        self._cie = CIEPipeline(self._config, self._nexus)
    return self._cie
