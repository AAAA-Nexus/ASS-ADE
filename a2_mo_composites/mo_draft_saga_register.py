# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:889
# Component id: mo.source.ass_ade.saga_register
from __future__ import annotations

__version__ = "0.1.0"

def saga_register(self, name: str, steps: list[str], compensations: list[str], **kwargs: Any) -> SagaCheckpoint:
    """/v1/rollback/saga — create saga blueprint (RBK-100). $0.040/call"""
    return self._post_model("/v1/rollback/saga", SagaCheckpoint, {
        "name": name, "steps": steps, "compensations": compensations, **kwargs,
    })
