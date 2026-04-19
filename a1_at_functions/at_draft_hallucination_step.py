# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:332
# Component id: at.source.ass_ade.hallucination_step
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
