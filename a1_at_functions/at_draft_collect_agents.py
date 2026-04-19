# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_collect_agents.py:7
# Component id: at.source.a1_at_functions.collect_agents
from __future__ import annotations

__version__ = "0.1.0"

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
