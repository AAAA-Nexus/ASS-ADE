# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_toolregistry.py:14
# Component id: og.source.ass_ade.get
__version__ = "0.1.0"

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)
