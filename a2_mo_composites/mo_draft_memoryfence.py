# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:682
# Component id: mo.source.ass_ade.memoryfence
from __future__ import annotations

__version__ = "0.1.0"

class MemoryFence(NexusModel):
    """/v1/memory/fence — MFN-100"""
    fence_id: str | None = None
    namespace: str | None = None
    hmac_key_set: bool | None = None
