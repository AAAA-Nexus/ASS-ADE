# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/tools/builtin.py:496
# Component id: mo.source.ass_ade.undoedittool
__version__ = "0.1.0"

class UndoEditTool:
    """Undo the last edit to a file, restoring its previous content."""

    def __init__(self, working_dir: str = ".", history: FileHistory | None = None) -> None:
        self._cwd = Path(working_dir).resolve()
        self._history = history

    @property
    def name(self) -> str:
        return "undo_edit"

    @property
    def description(self) -> str:
        return (
            "Undo the last write_file or edit_file operation on a file, "
            "restoring it to its previous content. Supports multiple undo steps."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path (relative to working directory) to undo.",
                },
            },
            "required": ["path"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        if self._history is None:
            return ToolResult(error="Undo history not available.", success=False)

        path_str = kwargs["path"]
        # Normalize to relative path
        resolved = _resolve(self._cwd, path_str)
        try:
            rel = str(resolved.relative_to(self._cwd))
        except ValueError:
            rel = path_str

        depth = self._history.depth(rel)
        if depth == 0:
            return ToolResult(error=f"No undo history for {path_str}", success=False)

        snap = self._history.undo(rel)
        if snap is None:
            return ToolResult(error=f"Failed to undo {path_str}", success=False)

        remaining = self._history.depth(rel)
        return ToolResult(
            output=f"Restored {path_str} to snapshot #{snap.sequence} ({remaining} undo steps remaining)"
        )
