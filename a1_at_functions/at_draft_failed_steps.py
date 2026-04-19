# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:68
# Component id: at.source.ass_ade.failed_steps
from __future__ import annotations

__version__ = "0.1.0"

def failed_steps(self) -> list[StepResult]:
    return [s for s in self.steps if s.status == StepStatus.FAILED]
