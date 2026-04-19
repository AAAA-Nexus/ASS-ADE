# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_stepstatus.py:7
# Component id: mo.source.a2_mo_composites.stepstatus
from __future__ import annotations

__version__ = "0.1.0"

class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
