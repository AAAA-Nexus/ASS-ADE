# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:708
# Component id: mo.source.a2_mo_composites.memory_fence_create
from __future__ import annotations

__version__ = "0.1.0"

def memory_fence_create(self, namespace: str, **kwargs: Any) -> MemoryFence:
    """/v1/memory/fence — cross-tenant HMAC namespace boundary (MFN-100). $0.040/call"""
    return self._post_model("/v1/memory/fence", MemoryFence, {"namespace": namespace, **kwargs})
