# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_plan.py:21
# Component id: at.source.ass_ade.executor
__version__ = "0.1.0"

def executor(workspace: Path) -> EditPlanExecutor:
    history = FileHistory(str(workspace))
    return EditPlanExecutor(str(workspace), history=history)
