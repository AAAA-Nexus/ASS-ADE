# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_stepfunction.py:5
# Component id: mo.source.ass_ade.stepfunction
__version__ = "0.1.0"

class StepFunction(Protocol):
    """Protocol for pipeline step functions.

    Takes a mutable context dict, performs work, and returns a StepResult.
    The step may add keys to context for downstream steps.
    """

    def __call__(self, context: dict[str, Any]) -> StepResult: ...
