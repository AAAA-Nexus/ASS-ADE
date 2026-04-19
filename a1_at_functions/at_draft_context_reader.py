# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_context_reader.py:7
# Component id: at.source.a1_at_functions.context_reader
from __future__ import annotations

__version__ = "0.1.0"

def context_reader(ctx: dict[str, Any]) -> StepResult:
    """Step that reads 'message' from context."""
    msg = ctx.get("message", "")
    return StepResult(
        name="reader", status=StepStatus.PASSED, output={"read_message": msg}
    )
