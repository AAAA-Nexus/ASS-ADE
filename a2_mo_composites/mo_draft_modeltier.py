# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_modeltier.py:7
# Component id: mo.source.a2_mo_composites.modeltier
from __future__ import annotations

__version__ = "0.1.0"

class ModelTier(str, Enum):
    FAST = "fast"
    STANDARD = "standard"
    DEEP = "deep"
