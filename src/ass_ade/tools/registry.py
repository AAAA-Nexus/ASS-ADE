"""Tool registry — discovers and manages tools."""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
from typing import Any

from ass_ade.engine.types import ToolSchema
from ass_ade.tools.base import Tool, ToolResult


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
        except (
            AttributeError,
            LookupError,
            OSError,
            RuntimeError,
            TypeError,
            ValueError,
        ) as exc:
            return ToolResult(output="", error=str(exc), success=False)


def _register_generated_tools(registry: ToolRegistry, working_dir: str) -> None:
    root = Path(working_dir).resolve()
    generated_dir = root / "src" / "ass_ade" / "tools" / "generated"
    if not generated_dir.is_dir():
        return

    for path in sorted(generated_dir.glob("*.py")):
        if path.name == "__init__.py":
            continue
        try:
            spec = importlib.util.spec_from_file_location(
                f"ass_ade_generated_tool_{path.stem}", path
            )
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except (AttributeError, ImportError, OSError, SyntaxError, ValueError):
            continue
        for _, candidate in inspect.getmembers(module, inspect.isclass):
            if not candidate.__name__.lower().endswith("tool"):
                continue
            try:
                tool = candidate(working_dir=working_dir)
            except TypeError:
                try:
                    tool = candidate(working_dir)
                except TypeError:
                    try:
                        tool = candidate()
                    except (
                        AttributeError,
                        OSError,
                        RuntimeError,
                        TypeError,
                        ValueError,
                    ):
                        continue
            except (AttributeError, OSError, RuntimeError, ValueError):
                continue
            if isinstance(tool, Tool):
                registry.register(tool)
                break


def default_registry(working_dir: str | None = None) -> ToolRegistry:
    """Create a registry pre-loaded with all built-in tools."""
    from ass_ade.tools.builtin import (
        EditFileTool,
        GrepSearchTool,
        ListDirectoryTool,
        ReadFileTool,
        RunCommandTool,
        SearchFilesTool,
        UndoEditTool,
        WriteFileTool,
    )
    from ass_ade.tools.history import FileHistory
    from ass_ade.tools.prompt import (
        PromptDiffTool,
        PromptHashTool,
        PromptProposeTool,
        PromptSectionTool,
        PromptValidateTool,
    )

    cwd = working_dir or "."

    # Initialize file history for undo support
    history = FileHistory(cwd)

    registry = ToolRegistry()
    registry.register(ReadFileTool(cwd))
    registry.register(WriteFileTool(cwd, history=history))
    registry.register(EditFileTool(cwd, history=history))
    registry.register(RunCommandTool(cwd))
    registry.register(ListDirectoryTool(cwd))
    registry.register(SearchFilesTool(cwd))
    registry.register(GrepSearchTool(cwd))
    registry.register(UndoEditTool(cwd, history=history))
    registry.register(PromptHashTool(cwd))
    registry.register(PromptValidateTool(cwd))
    registry.register(PromptSectionTool(cwd))
    registry.register(PromptDiffTool(cwd))
    registry.register(PromptProposeTool(cwd))
    _register_generated_tools(registry, cwd)
    return registry
