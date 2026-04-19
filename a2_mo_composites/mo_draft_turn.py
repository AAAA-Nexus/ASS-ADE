# Extracted from C:/!ass-ade/src/ass_ade/interpreter.py:497
# Component id: mo.source.ass_ade.turn
from __future__ import annotations

__version__ = "0.1.0"

class Turn:
    user: str
    tone: str
    intent: str
    path: str
    command: list[str]
    output: str
    response: str
