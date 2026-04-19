# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/capabilities.py:195
# Component id: at.source.ass_ade.render_capability_prompt_section
__version__ = "0.1.0"

def render_capability_prompt_section(
    working_dir: str | Path = ".",
    *,
    max_cli: int = 90,
    max_tools: int = 30,
    max_mcp: int = 40,
    max_agents: int = 20,
) -> str:
    snapshot = build_capability_snapshot(working_dir)
    lines = [
        "## Dynamic Capability Inventory",
        "",
        f"Generated from the current codebase at: {snapshot.generated_at_utc}",
        f"Working directory: {snapshot.working_dir}",
        "",
        "### CLI command paths",
        "",
        *_format_entries(snapshot.cli_commands, limit=max_cli),
        "",
        "### Local agent tools",
        "",
        *_format_entries(snapshot.local_tools, limit=max_tools),
        "",
        "### MCP stdio tools",
        "",
        *_format_entries(snapshot.mcp_tools, limit=max_mcp),
        "",
        "### Repo agents",
        "",
        *_format_entries(snapshot.agents, limit=max_agents),
    ]
    if snapshot.hooks:
        lines.extend(["", "### Hooks", "", *_format_entries(snapshot.hooks, limit=20)])
    return "\n".join(lines)
