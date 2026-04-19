# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:28
# Component id: at.source.ass_ade.counting_step
__version__ = "0.1.0"

def counting_step(ctx: dict[str, Any]) -> StepResult:
    count = ctx.get("count", 0)
    ctx["count"] = count + 1
    return StepResult(name="count", status=StepStatus.PASSED, output={"count": count + 1})
