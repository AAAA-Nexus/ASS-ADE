# Extracted from C:/!ass-ade/src/ass_ade/agent/capabilities.py:154
# Component id: at.source.ass_ade.collect_agents
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
