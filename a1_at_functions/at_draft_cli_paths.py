# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_capabilitysnapshot.py:15
# Component id: at.source.ass_ade.cli_paths
__version__ = "0.1.0"

    def cli_paths(self) -> set[str]:
        return {item.name for item in self.cli_commands}
