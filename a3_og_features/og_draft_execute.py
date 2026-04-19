# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_toolregistry.py:32
# Component id: og.source.a3_og_features.execute
from __future__ import annotations

__version__ = "0.1.0"

def execute(self, name: str, **kwargs: Any) -> ToolResult:
    tool = self._tools.get(name)
    if tool is None:
        return ToolResult(output="", error=f"Unknown tool: {name}", success=False)
    try:
        return tool.execute(**kwargs)
    except Exception as exc:
        return ToolResult(output="", error=str(exc), success=False)
