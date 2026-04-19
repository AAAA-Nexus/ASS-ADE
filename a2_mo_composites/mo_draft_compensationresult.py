# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:675
# Component id: mo.source.ass_ade.compensationresult
from __future__ import annotations

__version__ = "0.1.0"

class CompensationResult(NexusModel):
    """/v1/rollback/saga/{id}/compensate — RBK-100"""
    saga_id: str | None = None
    compensated_steps: list[str] = Field(default_factory=list)
    success: bool | None = None
