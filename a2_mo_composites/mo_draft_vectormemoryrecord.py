# Extracted from C:/!ass-ade/src/ass_ade/context_memory.py:45
# Component id: mo.source.ass_ade.vectormemoryrecord
from __future__ import annotations

__version__ = "0.1.0"

class VectorMemoryRecord(BaseModel):
    id: str
    namespace: str
    text: str
    vector: list[float]
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str
