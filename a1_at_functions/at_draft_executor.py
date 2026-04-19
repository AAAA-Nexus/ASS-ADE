# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_executor.py:7
# Component id: at.source.a1_at_functions.executor
from __future__ import annotations

__version__ = "0.1.0"

def executor(workspace: Path) -> EditPlanExecutor:
    history = FileHistory(str(workspace))
    return EditPlanExecutor(str(workspace), history=history)
