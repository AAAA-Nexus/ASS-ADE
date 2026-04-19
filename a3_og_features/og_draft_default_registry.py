# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/tools/registry.py:46
# Component id: og.source.ass_ade.default_registry
__version__ = "0.1.0"

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
    return registry
