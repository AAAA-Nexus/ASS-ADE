# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:38
# Component id: at.source.ass_ade.context_reader
__version__ = "0.1.0"

def context_reader(ctx: dict[str, Any]) -> StepResult:
    """Step that reads 'message' from context."""
    msg = ctx.get("message", "")
    return StepResult(
        name="reader", status=StepStatus.PASSED, output={"read_message": msg}
    )
