# Extracted from C:/!ass-ade/src/ass_ade/tools/base.py:10
# Component id: mo.source.ass_ade.toolresult
from __future__ import annotations

__version__ = "0.1.0"

class ToolResult(BaseModel):
    """Result of a tool execution."""

    output: str = ""
    error: str | None = None
    success: bool = True
