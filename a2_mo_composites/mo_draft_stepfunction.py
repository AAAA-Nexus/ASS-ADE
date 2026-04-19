# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_stepfunction.py:7
# Component id: mo.source.a2_mo_composites.stepfunction
from __future__ import annotations

__version__ = "0.1.0"

class StepFunction(Protocol):
    """Protocol for pipeline step functions.

    Takes a mutable context dict, performs work, and returns a StepResult.
    The step may add keys to context for downstream steps.
    """

    def __call__(self, context: dict[str, Any]) -> StepResult: ...
