# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_certify_pipeline.py:14
# Component id: at.source.ass_ade.hallucination_step
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
