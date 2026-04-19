# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:128
# Component id: at.source.ass_ade.step_names
from __future__ import annotations

__version__ = "0.1.0"

def step_names(self) -> list[str]:
    return [s.name for s in self._steps]
