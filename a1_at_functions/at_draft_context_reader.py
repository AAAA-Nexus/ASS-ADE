# Extracted from C:/!ass-ade/tests/test_pipeline.py:38
# Component id: at.source.ass_ade.context_reader
from __future__ import annotations

__version__ = "0.1.0"

def context_reader(ctx: dict[str, Any]) -> StepResult:
    """Step that reads 'message' from context."""
    msg = ctx.get("message", "")
    return StepResult(
        name="reader", status=StepStatus.PASSED, output={"read_message": msg}
    )
