# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_resolve_tool.py:7
# Component id: at.source.a1_at_functions.resolve_tool
from __future__ import annotations

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
