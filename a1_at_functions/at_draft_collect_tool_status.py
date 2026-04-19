# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_collect_tool_status.py:7
# Component id: at.source.a1_at_functions.collect_tool_status
from __future__ import annotations

__version__ = "0.1.0"

def collect_tool_status(tools: tuple[str, ...] = DEFAULT_TOOLS) -> list[ToolStatus]:
    return [detect_tool(tool) for tool in tools]
