# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_memory_fence_audit.py:7
# Component id: at.source.a1_at_functions.memory_fence_audit
from __future__ import annotations

__version__ = "0.1.0"

def memory_fence_audit(self, fence_id: str) -> MemoryFenceAudit:
    """/v1/memory/fence/{id}/audit — access log + entry count (MFN-100). $0.020/call"""
    return self._get_model(f"/v1/memory/fence/{_pseg(fence_id, 'fence_id')}/audit", MemoryFenceAudit)
