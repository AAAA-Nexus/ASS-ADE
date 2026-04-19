# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_toolcallrequest.py:7
# Component id: mo.source.a2_mo_composites.toolcallrequest
from __future__ import annotations

__version__ = "0.1.0"

class ToolCallRequest(BaseModel):
    """A tool invocation requested by a model."""

    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
