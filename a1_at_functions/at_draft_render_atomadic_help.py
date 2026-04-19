# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_render_atomadic_help.py:7
# Component id: at.source.a1_at_functions.render_atomadic_help
from __future__ import annotations

__version__ = "0.1.0"

def render_atomadic_help(working_dir: str | Path = ".") -> str:
    """Render a human help summary backed by the dynamic inventory."""
    snapshot = build_capability_snapshot(working_dir)
    highlighted = [
        item for item in snapshot.cli_commands
        if item.name in {
            "rebuild",
            "design",
            "docs",
            "lint",
            "certify",
            "enhance",
            "eco-scan",
            "recon",
            "doctor",
            "protocol evolution-record",
            "protocol evolution-demo",
            "protocol version-bump",
            "context pack",
            "context store",
            "context query",
            "mcp serve",
        }
    ]
    lines = [
        "I'm Atomadic, the front door of ASS-ADE.",
        "",
        "I learn my command and tool surface from the current codebase at runtime,",
        "so new CLI commands, local tools, MCP tools, agents, and hooks appear in",
        "my prompt without hand-editing a static list.",
        "",
        "Useful commands right now:",
        *_format_entries(highlighted, limit=40),
        "",
        "Local tools I can use:",
        *_format_entries(snapshot.local_tools, limit=20),
        "",
        "MCP workflow tools:",
        *_format_entries(snapshot.mcp_tools, limit=30),
        "",
        "Just tell me what you want in plain English.",
    ]
    return "\n".join(lines)
