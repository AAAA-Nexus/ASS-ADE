# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_certify_pipeline.py:27
# Component id: at.source.a1_at_functions.ethics_step
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
