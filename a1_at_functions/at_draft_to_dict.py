# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_to_dict.py:7
# Component id: at.source.a1_at_functions.to_dict
from __future__ import annotations

__version__ = "0.1.0"

def to_dict(self) -> dict[str, Any]:
    return {
        "user_profile": self.user_profile,
        "project_contexts": self.project_contexts,
        "preferences": self.preferences,
    }
