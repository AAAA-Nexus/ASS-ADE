# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_stepresult.py:7
# Component id: mo.source.a2_mo_composites.stepresult
from __future__ import annotations

__version__ = "0.1.0"

class StepResult:
    """Result of a single pipeline step."""

    name: str
    status: StepStatus
    output: dict[str, Any] = field(default_factory=dict)
    error: str = ""
    duration_ms: float = 0.0
