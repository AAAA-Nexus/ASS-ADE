# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_trust_gate_pipeline.py:32
# Component id: at.source.a1_at_functions.sybil_step
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
