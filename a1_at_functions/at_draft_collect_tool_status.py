# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_collect_tool_status.py:5
# Component id: at.source.ass_ade.collect_tool_status
__version__ = "0.1.0"

def collect_tool_status(tools: tuple[str, ...] = DEFAULT_TOOLS) -> list[ToolStatus]:
    return [detect_tool(tool) for tool in tools]
