# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_memorystore.py:72
# Component id: mo.source.a2_mo_composites.to_dict
from __future__ import annotations

__version__ = "0.1.0"

def to_dict(self) -> dict[str, Any]:
    return {
        "user_profile": self.user_profile,
        "project_contexts": self.project_contexts,
        "preferences": self.preferences,
    }
