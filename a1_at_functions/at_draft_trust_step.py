# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_trust_gate_pipeline.py:43
# Component id: at.source.a1_at_functions.trust_step
from __future__ import annotations

__version__ = "0.1.0"

def trust_step(ctx: dict[str, Any]) -> StepResult:
    try:
        result = client.trust_score(aid)
        raw = result.model_dump() if hasattr(result, "model_dump") else {}
        score = raw.get("score", 0)
        passed = score >= 0.5
        ctx["trust_score"] = score
        return StepResult(name="trust_score", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
    except Exception as exc:
        return StepResult(name="trust_score", status=StepStatus.FAILED, error=str(exc))
