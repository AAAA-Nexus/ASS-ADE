# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_counting_step.py:7
# Component id: at.source.a1_at_functions.counting_step
from __future__ import annotations

__version__ = "0.1.0"

def counting_step(ctx: dict[str, Any]) -> StepResult:
    count = ctx.get("count", 0)
    ctx["count"] = count + 1
    return StepResult(name="count", status=StepStatus.PASSED, output={"count": count + 1})
