# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/tools/registry.py:11
# Component id: og.source.ass_ade.toolregistry
__version__ = "0.1.0"

class ToolRegistry:
    """Registry of available tools."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[str]:
        return sorted(self._tools)

    def schemas(self) -> list[ToolSchema]:
        return [
            ToolSchema(
                name=t.name,
                description=t.description,
                parameters=t.parameters,
            )
            for t in self._tools.values()
        ]

    def execute(self, name: str, **kwargs: Any) -> ToolResult:
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(output="", error=f"Unknown tool: {name}", success=False)
        try:
            return tool.execute(**kwargs)
        except Exception as exc:
            return ToolResult(output="", error=str(exc), success=False)
