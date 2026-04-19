# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_trust_gate_pipeline.py:54
# Component id: at.source.a1_at_functions.reputation_step
from __future__ import annotations

__version__ = "0.1.0"

def reputation_step(ctx: dict[str, Any]) -> StepResult:
    try:
        result = client.reputation_score(aid)
        raw = result.model_dump() if hasattr(result, "model_dump") else {}
        ctx["reputation_tier"] = raw.get("tier")
        return StepResult(name="reputation_score", status=StepStatus.PASSED, output=raw)
    except Exception as exc:
        return StepResult(name="reputation_score", status=StepStatus.FAILED, error=str(exc))
