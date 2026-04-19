# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_toolschema.py:7
# Component id: qk.source.a0_qk_constants.toolschema
from __future__ import annotations

__version__ = "0.1.0"

class ToolSchema(BaseModel):
    """Describes a tool the model may invoke."""

    name: str
    description: str
    parameters: dict[str, Any]
