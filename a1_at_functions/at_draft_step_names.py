# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_step_names.py:7
# Component id: at.source.a1_at_functions.step_names
from __future__ import annotations

__version__ = "0.1.0"

def step_names(self) -> list[str]:
    return [s.name for s in self._steps]
