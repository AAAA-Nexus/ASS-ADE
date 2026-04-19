# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_pipeline.py:34
# Component id: at.source.ass_ade.error_step
__version__ = "0.1.0"

def error_step(ctx: dict[str, Any]) -> StepResult:
    raise RuntimeError("kaboom")
