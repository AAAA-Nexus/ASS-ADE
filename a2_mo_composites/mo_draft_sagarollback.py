# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:661
# Component id: mo.source.ass_ade.sagarollback
from __future__ import annotations

__version__ = "0.1.0"

class SagaRollback(NexusModel):
    """/v1/rollback/saga — RBK-100"""
    saga_id: str | None = None
    steps: list[str] = Field(default_factory=list)
    status: str | None = None
