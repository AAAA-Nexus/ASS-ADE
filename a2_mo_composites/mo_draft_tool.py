# Extracted from C:/!ass-ade/src/ass_ade/tools/base.py:19
# Component id: mo.source.ass_ade.tool
from __future__ import annotations

__version__ = "0.1.0"

class Tool(Protocol):
    """Protocol for ASS-ADE tools."""

    @property
    def name(self) -> str: ...

    @property
    def description(self) -> str: ...

    @property
    def parameters(self) -> dict[str, Any]: ...

    def execute(self, **kwargs: Any) -> ToolResult: ...
