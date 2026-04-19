"""Project context builder — gathers file and project information for system prompt."""

from __future__ import annotations

from pathlib import Path

from ass_ade.agent.capabilities import render_capability_prompt_section

SYSTEM_PROMPT_TEMPLATE = """\
You are ASS-ADE (Autonomous Sovereign Systems: Atomadic Development Environment), \
a military-grade agentic IDE that produces flawless code using any model.

You help users by reading, writing, and editing files, running commands, and \
searching codebases. You work methodically: read before editing, test after changing.

Working directory: {cwd}

{project_info}

{capability_info}

Rules:
- Read files before editing to understand existing code.
- Use edit_file for targeted changes (search/replace on exact text). Include 3+ lines of context.
- Use write_file only for creating new files.
- Run tests after making changes when a test suite exists.
- Use relative paths from the working directory.
- Be concise. Focus on action, not explanation.
- If a task is complex, break it into steps and execute them one at a time.
- When you are done, state what you did and what the user should verify.
- Treat the dynamic capability inventory as the source of truth for available
  ASS-ADE CLI commands and tools.
- Re-check the dynamic capability inventory whenever you need to decide what
  command, MCP tool, local tool, agent, or hook exists.
- When a user asks about your abilities, answer from the generated inventory
  and include the timestamp so they know it reflects the current codebase.
- Do not assume hosted `nexus_*` tools are available unless they appear in the
  inventory or are discovered through the MCP/Nexus discovery commands.
"""


def build_system_prompt(working_dir: str = ".") -> str:
    """Build the system prompt with project context."""
    cwd = Path(working_dir).resolve()
    project_info = _gather_project_info(cwd)
    capability_info = render_capability_prompt_section(cwd, max_cli=240, max_tools=40, max_mcp=50)
    return SYSTEM_PROMPT_TEMPLATE.format(
        cwd=cwd,
        project_info=project_info,
        capability_info=capability_info,
    )


def _gather_project_info(cwd: Path) -> str:
    """Gather project metadata from the working directory."""
    parts: list[str] = []

    # Detect project type
    markers = {
        "pyproject.toml": "Python",
        "package.json": "Node.js",
        "Cargo.toml": "Rust",
        "go.mod": "Go",
        "pom.xml": "Java (Maven)",
        "build.gradle": "Java (Gradle)",
    }
    for marker, lang in markers.items():
        if (cwd / marker).exists():
            parts.append(f"Project type: {lang} ({marker} found)")
            break

    # List top-level files/dirs
    skip = {".git", "node_modules", "__pycache__", ".venv", "venv", ".tox", ".mypy_cache"}
    try:
        entries = sorted(cwd.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except OSError:
        entries = []

    visible = [e for e in entries if e.name not in skip and not e.name.startswith(".")]
    if visible:
        listing = ", ".join(
            f"{e.name}/" if e.is_dir() else e.name for e in visible[:30]
        )
        parts.append(f"Top-level: {listing}")

    return "\n".join(parts) if parts else "No project metadata detected."
