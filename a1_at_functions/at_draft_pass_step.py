# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_pass_step.py:7
# Component id: at.source.a1_at_functions.pass_step
from __future__ import annotations

__version__ = "0.1.0"

def pass_step(ctx: dict[str, Any]) -> StepResult:
    ctx["pass_ran"] = True
    return StepResult(name="pass", status=StepStatus.PASSED, output={"ok": True})
