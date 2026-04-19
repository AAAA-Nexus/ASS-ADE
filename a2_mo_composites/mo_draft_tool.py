# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_tool.py:7
# Component id: mo.source.a2_mo_composites.tool
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
