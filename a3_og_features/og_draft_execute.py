# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_toolregistry.py:30
# Component id: og.source.ass_ade.execute
__version__ = "0.1.0"

    def execute(self, name: str, **kwargs: Any) -> ToolResult:
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(output="", error=f"Unknown tool: {name}", success=False)
        try:
            return tool.execute(**kwargs)
        except Exception as exc:
            return ToolResult(output="", error=str(exc), success=False)
