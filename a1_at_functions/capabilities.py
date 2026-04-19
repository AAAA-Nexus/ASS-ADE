"""Dynamic capability inventory for Atomadic prompts.

The interpreter should not rely on a stale, hand-written list of commands.
This module introspects the current Typer app, local tool registry, MCP server
tool schemas, and repo agent files so system prompts can reflect the code that
is actually present on disk.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class CapabilityEntry:
    kind: str
    name: str
    description: str = ""


@dataclass(frozen=True)
class CapabilitySnapshot:
    generated_at_utc: str
    working_dir: str
    cli_commands: list[CapabilityEntry] = field(default_factory=list)
    local_tools: list[CapabilityEntry] = field(default_factory=list)
    mcp_tools: list[CapabilityEntry] = field(default_factory=list)
    agents: list[CapabilityEntry] = field(default_factory=list)
    hooks: list[CapabilityEntry] = field(default_factory=list)

    @property
    def cli_paths(self) -> set[str]:
        return {item.name for item in self.cli_commands}

    @property
    def counts(self) -> dict[str, int]:
        return {
            "cli_commands": len(self.cli_commands),
            "local_tools": len(self.local_tools),
            "mcp_tools": len(self.mcp_tools),
            "agents": len(self.agents),
            "hooks": len(self.hooks),
        }

    @property
    def top_level_cli_groups(self) -> list[str]:
        return sorted({item.name.split()[0] for item in self.cli_commands if item.name})


def _first_sentence(text: str | None, *, limit: int = 120) -> str:
    clean = " ".join((text or "").strip().split())
    if not clean:
        return ""
    for sep in (". ", "\n"):
        if sep in clean:
            clean = clean.split(sep, 1)[0]
            break
    return clean[:limit].rstrip()


def _walk_click_command(command: Any, prefix: tuple[str, ...] = ()) -> list[CapabilityEntry]:
    entries: list[CapabilityEntry] = []
    commands = getattr(command, "commands", None)
    if not isinstance(commands, dict):
        return entries

    for name, subcommand in sorted(commands.items()):
        path = (*prefix, str(name))
        description = _first_sentence(
            getattr(subcommand, "short_help", None) or getattr(subcommand, "help", None)
        )
        entries.append(CapabilityEntry(kind="cli", name=" ".join(path), description=description))
        entries.extend(_walk_click_command(subcommand, path))
    return entries


def collect_cli_commands() -> list[CapabilityEntry]:
    """Return current CLI command paths by introspecting the Typer app."""
    try:
        click_root = _get_click_root()
        return _walk_click_command(click_root)
    except Exception:
        return []


def _get_click_root() -> Any:
    import typer.main

    from ass_ade.cli import app

    return typer.main.get_command(app)


def collect_local_tools(working_dir: str | Path = ".") -> list[CapabilityEntry]:
    """Return local agent tool schemas from the registered tool system."""
    try:
        from ass_ade.tools.registry import default_registry

        registry = default_registry(str(working_dir))
        return [
            CapabilityEntry(kind="tool", name=schema.name, description=_first_sentence(schema.description))
            for schema in registry.schemas()
        ]
    except Exception:
        return []


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


def _repo_root_from_working_dir(working_dir: str | Path) -> Path:
    cwd = Path(working_dir).resolve()
    for candidate in (cwd, *cwd.parents):
        if (candidate / "pyproject.toml").exists() or (candidate / "agents").is_dir():
            return candidate
    return cwd


def _read_agent_description(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("description:"):
            return _first_sentence(stripped.split(":", 1)[1])
    return ""


def collect_agents(working_dir: str | Path = ".") -> list[CapabilityEntry]:
    root = _repo_root_from_working_dir(working_dir)
    agents_dir = root / "agents"
    if not agents_dir.is_dir():
        return []
    entries: list[CapabilityEntry] = []
    for path in sorted(agents_dir.glob("*.agent.md")):
        entries.append(
            CapabilityEntry(
                kind="agent",
                name=path.stem.replace(".agent", ""),
                description=_read_agent_description(path),
            )
        )
    return entries


def collect_hooks(working_dir: str | Path = ".") -> list[CapabilityEntry]:
    root = _repo_root_from_working_dir(working_dir)
    hooks_dir = root / "hooks"
    if not hooks_dir.is_dir():
        return []
    return [
        CapabilityEntry(kind="hook", name=path.name, description="")
        for path in sorted(hooks_dir.glob("*.py"))
        if not path.name.startswith("_")
    ]


def build_capability_snapshot(working_dir: str | Path = ".") -> CapabilitySnapshot:
    cwd = str(Path(working_dir).resolve())
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    if now.endswith("+00:00"):
        now = f"{now[:-6]}Z"
    return CapabilitySnapshot(
        generated_at_utc=now,
        working_dir=cwd,
        cli_commands=collect_cli_commands(),
        local_tools=collect_local_tools(cwd),
        mcp_tools=collect_mcp_tools(cwd),
        agents=collect_agents(cwd),
        hooks=collect_hooks(cwd),
    )


def _format_entries(entries: Iterable[CapabilityEntry], *, limit: int, prefix: str = "-") -> list[str]:
    lines: list[str] = []
    for item in list(entries)[:limit]:
        if item.description:
            lines.append(f"{prefix} `{item.name}` - {item.description}")
        else:
            lines.append(f"{prefix} `{item.name}`")
    return lines or [f"{prefix} none detected"]


def _format_count_summary(snapshot: CapabilitySnapshot) -> list[str]:
    counts = snapshot.counts
    return [
        f"- CLI command paths: {counts['cli_commands']}",
        f"- Local agent tools: {counts['local_tools']}",
        f"- MCP stdio tools: {counts['mcp_tools']}",
        f"- Repo agents: {counts['agents']}",
        f"- Hooks: {counts['hooks']}",
    ]


def _format_top_level_cli_groups(snapshot: CapabilitySnapshot, *, limit: int = 60) -> str:
    groups = snapshot.top_level_cli_groups[:limit]
    if not groups:
        return "- none detected"
    rendered = ", ".join(f"`{name}`" for name in groups)
    extra = len(snapshot.top_level_cli_groups) - len(groups)
    if extra > 0:
        rendered = f"{rendered}, +{extra} more"
    return f"- {rendered}"


def _select_entries(entries: Iterable[CapabilityEntry], names: Iterable[str]) -> list[CapabilityEntry]:
    by_name = {entry.name: entry for entry in entries}
    return [by_name[name] for name in names if name in by_name]


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


def _find_repo_root(start: Path) -> Path | None:
    """Search upward from start for a git repo or pyproject.toml root."""
    current = start.resolve()
    for _ in range(10):
        if (current / ".git").exists() or (current / "pyproject.toml").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def _load_agent_md(repo_root: Path | None) -> str:
    """Read agents/atomadic_interpreter.md up to the auto-generated sections."""
    if repo_root is None:
        return ""
    md_path = repo_root / "agents" / "atomadic_interpreter.md"
    if not md_path.exists():
        return ""
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError:
        return ""
    for marker in ("## Current Capabilities", "## Dynamic Capability Inventory"):
        if marker in text:
            text = text[: text.index(marker)].rstrip()
            break
    return text.strip()


def _load_project_context_files(working_dir: Path) -> str:
    """Load ONBOARDING.md and RECON_REPORT.md from working_dir if present."""
    parts: list[str] = []
    for filename in ("ONBOARDING.md", "RECON_REPORT.md"):
        p = working_dir / filename
        if p.exists():
            try:
                content = p.read_text(encoding="utf-8")[:3000].strip()
                parts.append(f"### {filename}\n{content}")
            except OSError:
                pass
    return "\n\n".join(parts)


def build_atomadic_intent_prompt(
    working_dir: str | Path = ".",
    *,
    memory_context: str | None = None,
) -> str:
    """Build the live LLM intent-classifier prompt with current capabilities.

    Loads agents/atomadic_interpreter.md dynamically so changes to the agent
    definition are picked up without code modifications. Also incorporates
    any ONBOARDING.md or RECON_REPORT.md found in working_dir.
    """
    wdir = Path(working_dir).resolve()
    repo_root = _find_repo_root(wdir)

    agent_definition = _load_agent_md(repo_root)
    context_files = _load_project_context_files(wdir)
    capability_section = render_capability_prompt_section(
        working_dir,
        max_cli=240,
        max_tools=30,
        max_mcp=40,
        max_agents=20,
    )

    identity_block = agent_definition if agent_definition else (
        "You are Atomadic, the intelligent front door of ASS-ADE (Autonomous Sovereign\n"
        "System: Atomadic Development Environment), a CLI for analyzing, rebuilding,\n"
        "documenting, certifying, and evolving codebases."
    )

    extra_sections: list[str] = []
    if memory_context:
        extra_sections.append(f"## User Context\n{memory_context}")
    if context_files:
        extra_sections.append(f"## Project Onboarding Context\n{context_files}")
    extra_block = "\n\n".join(extra_sections)

    return f"""\
{identity_block}

{extra_block + chr(10) + chr(10) if extra_block else ""}\
Classify the user's message and respond with ONLY a single valid JSON object.
Do not use markdown fences. Do not add prose outside the JSON object.

Core front-door intents (read descriptions carefully to avoid misclassification):
- rebuild      — restructure an entire codebase into a clean 5-tier monadic layout
- design       — create a spec/blueprint for a NEW tool, feature, component, or idea (even if the user says "documentation tool" or "API"; the VERB is "design/plan/spec")
- add-feature  — add a new feature, endpoint, tool, skill, or component IN-PLACE to the current project (triggers: "add a …", "create a …", "build a …", "add an endpoint", "add health check")
- docs         — generate documentation (README, ARCHITECTURE, etc.) for EXISTING code
- lint         — check code quality, style, or bugs with static analysis (NOT for "scan this project" which is recon)
- certify      — sign or certify a codebase with a tamper-evident certificate
- enhance      — proactively scan for improvements and suggest/apply enhancements
- eco-scan     — monadic compliance check across the full ecosystem
- recon        — explore, survey, or understand what a repo contains (triggers: "scan this", "overview", "what's in this", "understand this")
- doctor       — health check: are tools, services, and connections working?
- self-enhance — evolve the CLI itself (add colors, ASCII art, spinners, progress bars)
- clean        — delete or purge old rebuild folders, backups, or evolved artifacts (triggers: "clean up", "delete old", "remove old", "purge")
- help         — list available commands and capabilities
- chat         — general conversation, questions about concepts

DISAMBIGUATION RULES:
- "design a [thing]" → design (not docs, even if [thing] contains the word "documentation")
- "scan this project" / "give me an overview" / "what's in this repo" → recon (not lint)
- "add a [noun]" / "add an [noun]" / "create a [noun]" → add-feature (not lint, even if noun is "health check")
- "clean up old rebuild" / "delete old builds" → clean (not rebuild)
- "check code quality" / "find bugs" / "fix bugs" / "what's wrong" / "run linter" → lint (not rebuild, not recon)
- "make it faster" / "speed this up" / "optimize" / "improve performance" → enhance (NOT rebuild)
- "fix the bugs" / "there are bugs" / "fix issues" → lint (NOT rebuild)
- rebuild is ONLY for explicit whole-project restructuring: the user must say "rebuild", "restructure", "reorganize", "rewrite", or "overhaul". Vague improvement requests are NEVER rebuild.

If the message maps to a core front-door intent:
  {{"type":"command","intent":"<core intent>","path":"<input path or null>","output_path":"<output path or null, only for rebuild>","feature_desc":"<feature description or null>"}}

If the message maps to another known ASS-ADE CLI command from the dynamic
inventory, dispatch it exactly through cli_args:
  {{"type":"command","intent":"cli","cli_args":["protocol","evolution-record"],"path":null,"output_path":null,"feature_desc":null}}

If the user asks what commands are available, what you can do, or says "help":
  {{"type":"command","intent":"help","path":null,"output_path":null,"feature_desc":null}}

If the message is general conversation:
  {{"type":"chat","response":"<short conversational reply>"}}

Prefer exact CLI command paths from the inventory. Do not invent command names.
For file paths, preserve user-provided [datetime] or {{datetime}} tokens exactly.

{capability_section}
"""


def command_path_exists(args: list[str], working_dir: str | Path = ".") -> bool:
    """Return True if args starts with a known CLI command path."""
    if not args:
        return False
    tokens = [str(item).strip() for item in args if str(item).strip()]
    if not tokens:
        return False
    try:
        command = _get_click_root()
    except Exception:
        snapshot = build_capability_snapshot(working_dir)
        return " ".join(tokens[:1]) in snapshot.cli_paths

    matched = 0
    while matched < len(tokens):
        commands = getattr(command, "commands", None)
        if not isinstance(commands, dict):
            break
        next_token = tokens[matched]
        if next_token not in commands:
            break
        command = commands[next_token]
        matched += 1

    if matched == 0:
        return False
    if matched == len(tokens):
        return True

    # A group with subcommands should not accept an unknown subcommand token.
    remaining = tokens[matched:]
    if getattr(command, "commands", None) and remaining and not remaining[0].startswith("-"):
        return False
    return True


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
        f"Inventory generated at: {snapshot.generated_at_utc}",
        "",
        "Capability counts:",
        *_format_count_summary(snapshot),
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


def render_markdown_capability_section(working_dir: str | Path = ".") -> str:
    return (
        "---\n\n"
        "## Current Capabilities\n\n"
        "*Auto-generated from the live CLI, tool registry, MCP server, agents, and hooks.*\n\n"
        f"{render_capability_prompt_section(working_dir, max_cli=160, max_tools=60, max_mcp=80)}\n"
    )


def sync_atomadic_prompt_capabilities(
    *,
    repo_root: str | Path = ".",
    prompt_path: str | Path = "agents/atomadic_interpreter.md",
) -> Path:
    """Refresh the generated capability block in the Atomadic prompt artifact."""
    root = Path(repo_root).resolve()
    target = Path(prompt_path)
    if not target.is_absolute():
        target = root / target
    target.parent.mkdir(parents=True, exist_ok=True)
    marker = "\n---\n\n## Current Capabilities"
    if target.exists():
        text = target.read_text(encoding="utf-8")
        if marker in text:
            text = text[: text.index(marker)].rstrip()
    else:
        text = "# Atomadic Nexus Interpreter\n"
    target.write_text(
        f"{text.rstrip()}\n\n{render_markdown_capability_section(root)}",
        encoding="utf-8",
    )
    return target
