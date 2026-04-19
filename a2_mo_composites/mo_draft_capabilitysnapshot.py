# Extracted from C:/!ass-ade/src/ass_ade/agent/capabilities.py:25
# Component id: mo.source.ass_ade.capabilitysnapshot
from __future__ import annotations

__version__ = "0.1.0"

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
