# Extracted from C:/!ass-ade/tests/test_pipeline.py:24
# Component id: at.source.ass_ade.fail_step
from __future__ import annotations

__version__ = "0.1.0"

def fail_step(ctx: dict[str, Any]) -> StepResult:
    return StepResult(name="fail", status=StepStatus.FAILED, error="something broke")
