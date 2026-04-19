# Extracted from C:/!ass-ade/src/ass_ade/agent/ide.py:9
# Component id: mo.source.ass_ade.candidate
from __future__ import annotations

__version__ = "0.1.0"

class Candidate:
    id: str
    features: tuple[int, int]
    fitness: float
    payload: dict = field(default_factory=dict)
