# Extracted from C:/!ass-ade/src/ass_ade/agent/capabilities.py:236
# Component id: at.source.ass_ade.render_capability_prompt_section
from __future__ import annotations

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
    highlighted_cli = _select_entries(
        snapshot.cli_commands,
        [
            "doctor",
            "recon",
            "eco-scan",
            "context pack",
            "context store",
            "context query",
            "design",
            "rebuild",
            "enhance",
            "lint",
            "certify",
            "protocol evolution-record",
            "protocol evolution-demo",
            "protocol version-bump",
            "prompt sync-agent",
            "mcp serve",
            "mcp tools",
            "nexus overview",
            "nexus mcp-manifest",
        ],
    )
    nexus_mcp_tools = [item for item in snapshot.mcp_tools if item.name.startswith("nexus_")]
    lines = [
        "## Dynamic Capability Inventory",
        "",
        "This section is generated at prompt-build time from the code on disk.",
        "Treat it as the authoritative capability map for this session.",
        "",
        f"Generated at: {snapshot.generated_at_utc}",
        f"Working directory: {snapshot.working_dir}",
        "",
        "### Capability summary",
        "",
        *_format_count_summary(snapshot),
        "",
        "### Top-level CLI groups",
        "",
        _format_top_level_cli_groups(snapshot),
        "",
        "### Runtime routing rules",
        "",
        "- Prefer exact command paths listed in this inventory over static examples or memory.",
        "- If a user asks what Atomadic can do, answer from this inventory and mention its generated timestamp.",
        "- For CLI dispatch, emit command tokens that begin with one of the listed command paths.",
        "- For tools, use only local agent tools or MCP tools listed below unless a live discovery command adds more.",
        "- Hosted `nexus_*` MCP tools must appear here or be discovered with `mcp tools` / `nexus mcp-manifest` before use.",
        "- When a needed capability is absent, use `map_terrain`, `phase0_recon`, or a clarifying question instead of inventing it.",
        "",
        "### High-signal command paths",
        "",
        *_format_entries(highlighted_cli, limit=40),
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
        "### Hosted Nexus MCP tools discovered in this session",
        "",
        *_format_entries(nexus_mcp_tools, limit=max_mcp),
        "",
        "### Repo agents",
        "",
        *_format_entries(snapshot.agents, limit=max_agents),
    ]
    if snapshot.hooks:
        lines.extend(["", "### Hooks", "", *_format_entries(snapshot.hooks, limit=20)])
    return "\n".join(lines)
