# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/pipeline.py:361
# Component id: at.source.ass_ade.certify_step
__version__ = "0.1.0"

    def certify_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.certify_output(text, rubric=["accuracy", "safety", "compliance"])
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            ctx["certificate_id"] = raw.get("certificate_id")
            return StepResult(name="certify_output", status=StepStatus.PASSED, output=raw)
        except Exception as exc:
            return StepResult(name="certify_output", status=StepStatus.FAILED, error=str(exc))
