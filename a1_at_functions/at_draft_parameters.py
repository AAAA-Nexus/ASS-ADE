# Extracted from C:/!ass-ade/src/ass_ade/tools/prompt.py:113
# Component id: at.source.ass_ade.parameters
from __future__ import annotations

__version__ = "0.1.0"

def parameters(self) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "prompt_path": {"type": "string", "description": "Repo-relative prompt file."},
            "prompt_text": {"type": "string", "description": "Inline prompt text."},
        },
    }
