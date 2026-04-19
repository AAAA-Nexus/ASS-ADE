# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_add.py:7
# Component id: at.source.a1_at_functions.add
from __future__ import annotations

__version__ = "0.1.0"

def add(self, name: str, fn: StepFunction) -> Pipeline:
    """Add a step to the pipeline. Returns self for chaining."""
    self._steps.append(_StepEntry(name=name, fn=fn))
    return self
