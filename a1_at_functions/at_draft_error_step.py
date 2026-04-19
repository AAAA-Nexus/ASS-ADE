# Extracted from C:/!ass-ade/tests/test_pipeline.py:34
# Component id: at.source.ass_ade.error_step
from __future__ import annotations

__version__ = "0.1.0"

def error_step(ctx: dict[str, Any]) -> StepResult:
    raise RuntimeError("kaboom")
