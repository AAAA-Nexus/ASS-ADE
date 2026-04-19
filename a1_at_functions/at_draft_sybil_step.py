# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:255
# Component id: at.source.ass_ade.sybil_step
from __future__ import annotations

__version__ = "0.1.0"

def sybil_step(ctx: dict[str, Any]) -> StepResult:
    try:
        result = client.sybil_check(aid)
        raw = result.model_dump() if hasattr(result, "model_dump") else {}
        risk = raw.get("sybil_risk", "low")
        passed = risk != "high"
        ctx["sybil_passed"] = passed
        return StepResult(name="sybil_check", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
    except Exception as exc:
        return StepResult(name="sybil_check", status=StepStatus.FAILED, error=str(exc))
