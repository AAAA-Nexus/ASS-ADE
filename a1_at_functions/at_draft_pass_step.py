# Extracted from C:/!ass-ade/tests/test_pipeline.py:19
# Component id: at.source.ass_ade.pass_step
from __future__ import annotations

__version__ = "0.1.0"

def pass_step(ctx: dict[str, Any]) -> StepResult:
    ctx["pass_ran"] = True
    return StepResult(name="pass", status=StepStatus.PASSED, output={"ok": True})
