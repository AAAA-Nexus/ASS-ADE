# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_collect_mcp_tools.py:7
# Component id: sy.source.a4_sy_orchestration.collect_mcp_tools
from __future__ import annotations

__version__ = "0.1.0"

def collect_mcp_tools(working_dir: str | Path = ".") -> list[CapabilityEntry]:
    """Return the local MCP tool surface exposed by the stdio server."""
    entries = {
        item.name: item
        for item in collect_local_tools(working_dir)
    }
    try:
        from ass_ade.mcp.server import _WORKFLOW_TOOLS

        for tool in _WORKFLOW_TOOLS:
            name = str(tool.get("name", "")).strip()
            if not name:
                continue
            entries[name] = CapabilityEntry(
                kind="mcp",
                name=name,
                description=_first_sentence(str(tool.get("description", ""))),
            )
    except Exception:
        pass
    return sorted(entries.values(), key=lambda item: item.name)
