# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_certify_pipeline.py:16
# Component id: at.source.a1_at_functions.hallucination_step
from __future__ import annotations

__version__ = "0.1.0"

def hallucination_step(ctx: dict[str, Any]) -> StepResult:
    try:
        result = client.hallucination_oracle(text)
        raw = result.model_dump() if hasattr(result, "model_dump") else {}
        verdict = raw.get("verdict", "unknown")
        passed = verdict not in ("unsafe", "error")
        ctx["hallucination_verdict"] = verdict
        return StepResult(name="hallucination_oracle", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
    except Exception as exc:
        return StepResult(name="hallucination_oracle", status=StepStatus.FAILED, error=str(exc))
