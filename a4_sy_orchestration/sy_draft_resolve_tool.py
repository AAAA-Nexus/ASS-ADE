# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/mcp/utils.py:23
# Component id: sy.source.ass_ade.resolve_tool
__version__ = "0.1.0"

def resolve_tool(manifest: MCPManifest, identifier: str) -> MCPTool | None:
    """Resolve a tool by index (1-based) or name.

    identifier may be a numeric string referencing the manifest list index,
    or a tool name.
    """
    if identifier.isdigit():
        idx = int(identifier) - 1
        if 0 <= idx < len(manifest.tools):
            return manifest.tools[idx]
        return None

    for tool in manifest.tools:
        if tool.name and tool.name.lower() == identifier.lower():
            return tool
    return None
