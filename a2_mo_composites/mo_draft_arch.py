# Extracted from C:/!ass-ade/src/ass_ade/agent/severa.py:9
# Component id: mo.source.ass_ade.arch
from __future__ import annotations

__version__ = "0.1.0"

class Arch:
    name: str
    score: float
    traits: list[str] = field(default_factory=list)
