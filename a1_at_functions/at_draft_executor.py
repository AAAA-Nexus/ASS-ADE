# Extracted from C:/!ass-ade/tests/test_plan.py:21
# Component id: at.source.ass_ade.executor
from __future__ import annotations

__version__ = "0.1.0"

def executor(workspace: Path) -> EditPlanExecutor:
    history = FileHistory(str(workspace))
    return EditPlanExecutor(str(workspace), history=history)
