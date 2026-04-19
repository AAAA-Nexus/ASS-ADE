# Extracted from C:/!ass-ade/src/ass_ade/system.py:44
# Component id: sy.source.ass_ade.collect_tool_status
from __future__ import annotations

__version__ = "0.1.0"

def collect_tool_status(tools: tuple[str, ...] = DEFAULT_TOOLS) -> list[ToolStatus]:
    return [detect_tool(tool) for tool in tools]
