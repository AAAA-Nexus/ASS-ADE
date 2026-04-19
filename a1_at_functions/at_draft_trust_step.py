# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/pipeline.py:266
# Component id: at.source.ass_ade.trust_step
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
