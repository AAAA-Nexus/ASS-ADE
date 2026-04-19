# Extracted from C:/!ass-ade/src/ass_ade/engine/types.py:10
# Component id: mo.source.ass_ade.toolcallrequest
from __future__ import annotations

__version__ = "0.1.0"

class ToolCallRequest(BaseModel):
    """A tool invocation requested by a model."""

    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
