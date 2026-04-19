# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_streamevent.py:7
# Component id: mo.source.a2_mo_composites.streamevent
from __future__ import annotations

__version__ = "0.1.0"

class StreamEvent:
    """An event emitted during streaming agent execution."""

    kind: Literal["token", "tool_call", "tool_result", "blocked", "done", "error"]
    text: str = ""
    tool_name: str = ""
    tool_args: dict[str, Any] = field(default_factory=dict)
    tool_result: ToolResult | None = None
