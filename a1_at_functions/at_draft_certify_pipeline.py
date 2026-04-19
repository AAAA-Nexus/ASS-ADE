# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:323
# Component id: at.source.ass_ade.certify_pipeline
from __future__ import annotations

__version__ = "0.1.0"

def certify_pipeline(
    client: Any,
    text: str,
    *,
    on_progress: ProgressCallback | None = None,
    persist_dir: str | None = None,
) -> Pipeline:
    """Build a certification pipeline: hallucination → ethics → compliance → certify."""

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

    def ethics_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.ethics_check(text)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            passed = raw.get("safe", False)
            return StepResult(name="ethics_check", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
        except Exception as exc:
            return StepResult(name="ethics_check", status=StepStatus.FAILED, error=str(exc))

    def compliance_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.compliance_check(text)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            passed = raw.get("compliant", False)
            return StepResult(name="compliance_check", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
        except Exception as exc:
            return StepResult(name="compliance_check", status=StepStatus.FAILED, error=str(exc))

    def certify_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.certify_output(text, rubric=["accuracy", "safety", "compliance"])
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            ctx["certificate_id"] = raw.get("certificate_id")
            return StepResult(name="certify_output", status=StepStatus.PASSED, output=raw)
        except Exception as exc:
            return StepResult(name="certify_output", status=StepStatus.FAILED, error=str(exc))

    pipe = Pipeline(
        "certify-output",
        fail_fast=False,
        persist_dir=persist_dir,
        on_progress=on_progress,
    )
    pipe.add("hallucination_oracle", hallucination_step)
    pipe.add("ethics_check", ethics_step)
    pipe.add("compliance_check", compliance_step)
    pipe.add("certify_output", certify_step)
    return pipe
