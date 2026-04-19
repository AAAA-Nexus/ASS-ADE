# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:47
# Component id: mo.source.ass_ade.stepresult
from __future__ import annotations

__version__ = "0.1.0"

class StepResult:
    """Result of a single pipeline step."""

    name: str
    status: StepStatus
    output: dict[str, Any] = field(default_factory=dict)
    error: str = ""
    duration_ms: float = 0.0
