# Extracted from C:/!ass-ade/src/ass_ade/context_memory.py:69
# Component id: mo.source.ass_ade.vectormemoryqueryresult
from __future__ import annotations

__version__ = "0.1.0"

class VectorMemoryQueryResult(BaseModel):
    query: str
    namespace: str
    matches: list[VectorMemoryMatch] = Field(default_factory=list)
