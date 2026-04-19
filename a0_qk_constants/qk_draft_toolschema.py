# Extracted from C:/!ass-ade/src/ass_ade/engine/types.py:28
# Component id: qk.source.ass_ade.toolschema
from __future__ import annotations

__version__ = "0.1.0"

class ToolSchema(BaseModel):
    """Describes a tool the model may invoke."""

    name: str
    description: str
    parameters: dict[str, Any]
