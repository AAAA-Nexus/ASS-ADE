# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:245
# Component id: at.source.ass_ade.identity_step
from __future__ import annotations

__version__ = "0.1.0"

def identity_step(ctx: dict[str, Any]) -> StepResult:
    try:
        result = client.identity_verify(aid)
        raw = result.model_dump() if hasattr(result, "model_dump") else {}
        passed = raw.get("decision", "allow") != "deny"
        ctx["identity_passed"] = passed
        return StepResult(name="identity_verify", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
    except Exception as exc:
        return StepResult(name="identity_verify", status=StepStatus.FAILED, error=str(exc))
