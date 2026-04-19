# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_toolregistry.py:11
# Component id: og.source.ass_ade.register
__version__ = "0.1.0"

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool
