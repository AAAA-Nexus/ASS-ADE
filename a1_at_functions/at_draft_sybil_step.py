# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_trust_gate_pipeline.py:30
# Component id: at.source.ass_ade.sybil_step
__version__ = "0.1.0"

    def sybil_step(ctx: dict[str, Any]) -> StepResult:
        try:
            result = client.sybil_check(aid)
            raw = result.model_dump() if hasattr(result, "model_dump") else {}
            risk = raw.get("sybil_risk", "low")
            passed = risk != "high"
            ctx["sybil_passed"] = passed
            return StepResult(name="sybil_check", status=StepStatus.PASSED if passed else StepStatus.FAILED, output=raw)
        except Exception as exc:
            return StepResult(name="sybil_check", status=StepStatus.FAILED, error=str(exc))
