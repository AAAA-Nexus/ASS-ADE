# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_capabilitysnapshot.py:7
# Component id: mo.source.a2_mo_composites.capabilitysnapshot
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
