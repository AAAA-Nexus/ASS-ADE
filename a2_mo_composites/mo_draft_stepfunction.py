# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:81
# Component id: mo.source.ass_ade.stepfunction
from __future__ import annotations

__version__ = "0.1.0"

class StepFunction(Protocol):
    """Protocol for pipeline step functions.

    Takes a mutable context dict, performs work, and returns a StepResult.
    The step may add keys to context for downstream steps.
    """

    def __call__(self, context: dict[str, Any]) -> StepResult: ...
