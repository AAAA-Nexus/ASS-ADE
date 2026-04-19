# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:277
# Component id: at.source.ass_ade.reputation_step
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
