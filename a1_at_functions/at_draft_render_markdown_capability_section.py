# Extracted from C:/!ass-ade/src/ass_ade/agent/capabilities.py:534
# Component id: at.source.ass_ade.render_markdown_capability_section
from __future__ import annotations

__version__ = "0.1.0"

def render_markdown_capability_section(working_dir: str | Path = ".") -> str:
    return (
        "---\n\n"
        "## Current Capabilities\n\n"
        "*Auto-generated from the live CLI, tool registry, MCP server, agents, and hooks.*\n\n"
        f"{render_capability_prompt_section(working_dir, max_cli=160, max_tools=60, max_mcp=80)}\n"
    )
