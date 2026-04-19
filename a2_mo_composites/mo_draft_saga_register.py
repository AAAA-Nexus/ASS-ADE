# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:694
# Component id: mo.source.a2_mo_composites.saga_register
from __future__ import annotations

__version__ = "0.1.0"

def saga_register(self, name: str, steps: list[str], compensations: list[str], **kwargs: Any) -> SagaCheckpoint:
    """/v1/rollback/saga — create saga blueprint (RBK-100). $0.040/call"""
    return self._post_model("/v1/rollback/saga", SagaCheckpoint, {
        "name": name, "steps": steps, "compensations": compensations, **kwargs,
    })
