# Extracted from C:/!ass-ade/src/ass_ade/interpreter.py:254
# Component id: at.source.ass_ade.to_dict
from __future__ import annotations

__version__ = "0.1.0"

def to_dict(self) -> dict[str, Any]:
    return {
        "user_profile": self.user_profile,
        "project_contexts": self.project_contexts,
        "preferences": self.preferences,
    }
