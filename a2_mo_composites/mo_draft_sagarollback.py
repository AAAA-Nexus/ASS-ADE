# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_sagarollback.py:7
# Component id: mo.source.a2_mo_composites.sagarollback
from __future__ import annotations

__version__ = "0.1.0"

class SagaRollback(NexusModel):
    """/v1/rollback/saga — RBK-100"""
    saga_id: str | None = None
    steps: list[str] = Field(default_factory=list)
    status: str | None = None
