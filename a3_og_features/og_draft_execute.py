# Extracted from C:/!ass-ade/src/ass_ade/tools/registry.py:39
# Component id: og.source.ass_ade.execute
from __future__ import annotations

__version__ = "0.1.0"

def execute(self, name: str, **kwargs: Any) -> ToolResult:
    tool = self._tools.get(name)
    if tool is None:
        return ToolResult(output="", error=f"Unknown tool: {name}", success=False)
    try:
        return tool.execute(**kwargs)
    except (
        AttributeError,
        LookupError,
        OSError,
        RuntimeError,
        TypeError,
        ValueError,
    ) as exc:
        return ToolResult(output="", error=str(exc), success=False)
