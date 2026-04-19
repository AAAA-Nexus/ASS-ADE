# Extracted from C:/!ass-ade/src/ass_ade/agent/atlas.py:9
# Component id: mo.source.ass_ade.subtask
from __future__ import annotations

__version__ = "0.1.0"

class SubTask:
    id: str
    description: str
    priority: float
    deps: list[str] = field(default_factory=list)
