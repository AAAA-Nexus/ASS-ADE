# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_memoryfence.py:7
# Component id: mo.source.a2_mo_composites.memoryfence
from __future__ import annotations

__version__ = "0.1.0"

class MemoryFence(NexusModel):
    """/v1/memory/fence — MFN-100"""
    fence_id: str | None = None
    namespace: str | None = None
    hmac_key_set: bool | None = None
