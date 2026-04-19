# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/capabilities.py:25
# Component id: mo.source.ass_ade.capabilitysnapshot
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
