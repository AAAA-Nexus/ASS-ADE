# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:343
# Component id: at.source.ass_ade.ethics_step
from __future__ import annotations

__version__ = "0.1.0"

def ethics_step(ctx: dict[str, Any]) -> StepResult:
    try:
        result = client.ethics_check(text)
        raw = result.model_dump() if hasattr(result, "model_dump") else {}
        passed = raw.get("safe", False)
        return StepResult(name="ethics_check", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
    except Exception as exc:
        return StepResult(name="ethics_check", status=StepStatus.FAILED, error=str(exc))
