# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_certify_pipeline.py:45
# Component id: at.source.a1_at_functions.certify_step
from __future__ import annotations

__version__ = "0.1.0"

def certify_step(ctx: dict[str, Any]) -> StepResult:
    try:
        result = client.certify_output(text, rubric=["accuracy", "safety", "compliance"])
        raw = result.model_dump() if hasattr(result, "model_dump") else {}
        ctx["certificate_id"] = raw.get("certificate_id")
        return StepResult(name="certify_output", status=StepStatus.PASSED, output=raw)
    except Exception as exc:
        return StepResult(name="certify_output", status=StepStatus.FAILED, error=str(exc))
