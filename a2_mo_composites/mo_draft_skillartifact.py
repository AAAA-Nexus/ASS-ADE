# Extracted from C:/!ass-ade/src/ass_ade/agent/exif.py:11
# Component id: mo.source.ass_ade.skillartifact
from __future__ import annotations

__version__ = "0.1.0"

class SkillArtifact:
    skill: str
    feasibility: float
    samples: int
    trace: list[dict] = field(default_factory=list)
    ready: bool = False
