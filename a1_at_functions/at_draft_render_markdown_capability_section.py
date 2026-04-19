# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_render_markdown_capability_section.py:7
# Component id: at.source.a1_at_functions.render_markdown_capability_section
from __future__ import annotations

__version__ = "0.1.0"

def render_markdown_capability_section(working_dir: str | Path = ".") -> str:
    return (
        "---\n\n"
        "## Current Capabilities\n\n"
        "*Auto-generated from the live CLI, tool registry, MCP server, agents, and hooks.*\n\n"
        f"{render_capability_prompt_section(working_dir, max_cli=160, max_tools=60, max_mcp=80)}\n"
    )
