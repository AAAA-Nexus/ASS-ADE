# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_toolregistry.py:20
# Component id: qk.source.ass_ade.schemas
__version__ = "0.1.0"

    def schemas(self) -> list[ToolSchema]:
        return [
            ToolSchema(
                name=t.name,
                description=t.description,
                parameters=t.parameters,
            )
            for t in self._tools.values()
        ]
