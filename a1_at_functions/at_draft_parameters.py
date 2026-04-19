# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_grepsearchtool.py:22
# Component id: at.source.a2_mo_composites.parameters
from __future__ import annotations

__version__ = "0.1.0"

def parameters(self) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "pattern": {"type": "string", "description": "Regex pattern (case-insensitive)."},
            "include": {
                "type": "string",
                "description": "Glob to filter files (e.g., '**/*.py'). Default: all files.",
            },
        },
        "required": ["pattern"],
    }
