# Extracted from C:/!ass-ade/src/ass_ade/agent/atlas.py:24
# Component id: at.source.ass_ade.complexity_score
from __future__ import annotations

__version__ = "0.1.0"

def complexity_score(spec: str, fan_out: int = 0) -> float:
    return len(spec) / 1000.0 + fan_out / 10.0
