# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_arch.py:7
# Component id: mo.source.a2_mo_composites.arch
from __future__ import annotations

__version__ = "0.1.0"

class Arch:
    name: str
    score: float
    traits: list[str] = field(default_factory=list)
