# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_saga_checkpoint.py:7
# Component id: at.source.a1_at_functions.saga_checkpoint
from __future__ import annotations

__version__ = "0.1.0"

def saga_checkpoint(self, saga_id: str, step: str, **kwargs: Any) -> SagaCheckpoint:
    """/v1/rollback/saga/{id}/checkpoint — mark step completed (RBK-100). $0.020/call"""
    return self._post_model(f"/v1/rollback/saga/{_pseg(saga_id, 'saga_id')}/checkpoint", SagaCheckpoint, {"step": step, **kwargs})
