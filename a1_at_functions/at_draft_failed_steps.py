# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_failed_steps.py:7
# Component id: at.source.a1_at_functions.failed_steps
from __future__ import annotations

__version__ = "0.1.0"

def failed_steps(self) -> list[StepResult]:
    return [s for s in self.steps if s.status == StepStatus.FAILED]
