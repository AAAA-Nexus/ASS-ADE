# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:352
# Component id: at.source.ass_ade.compliance_step
from __future__ import annotations

__version__ = "0.1.0"

def compliance_step(ctx: dict[str, Any]) -> StepResult:
    try:
        result = client.compliance_check(text)
        raw = result.model_dump() if hasattr(result, "model_dump") else {}
        passed = raw.get("compliant", False)
        return StepResult(name="compliance_check", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
    except Exception as exc:
        return StepResult(name="compliance_check", status=StepStatus.FAILED, error=str(exc))
