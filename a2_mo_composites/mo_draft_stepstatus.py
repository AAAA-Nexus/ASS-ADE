# Extracted from C:/!ass-ade/src/ass_ade/pipeline.py:38
# Component id: mo.source.ass_ade.stepstatus
from __future__ import annotations

__version__ = "0.1.0"

class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
