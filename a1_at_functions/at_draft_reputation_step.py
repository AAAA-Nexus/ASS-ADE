# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_trust_gate_pipeline.py:52
# Component id: at.source.ass_ade.reputation_step
__version__ = "0.1.0"

    def reputation_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.reputation_score(aid)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            ctx["reputation_tier"] = raw.get("tier")
            return StepResult(name="reputation_score", status=StepStatus.PASSED, output=raw)
        except Exception as exc:
            return StepResult(name="reputation_score", status=StepStatus.FAILED, error=str(exc))
