# Extracted from C:/!ass-ade/src/ass_ade/context_memory.py:60
# Component id: mo.source.ass_ade.vectormemorymatch
from __future__ import annotations

__version__ = "0.1.0"

class VectorMemoryMatch(BaseModel):
    id: str
    namespace: str
    score: float
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str
