# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_compensationresult.py:7
# Component id: mo.source.a2_mo_composites.compensationresult
from __future__ import annotations

__version__ = "0.1.0"

class CompensationResult(NexusModel):
    """/v1/rollback/saga/{id}/compensate — RBK-100"""
    saga_id: str | None = None
    compensated_steps: list[str] = Field(default_factory=list)
    success: bool | None = None
