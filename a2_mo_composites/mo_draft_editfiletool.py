# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/tools/builtin.py:155
# Component id: mo.source.ass_ade.editfiletool
__version__ = "0.1.0"

class EditFileTool:
    """Search-and-replace edit in a file.

    The ``old_string`` must match exactly one location in the file.
    """

    def __init__(self, working_dir: str = ".", history: FileHistory | None = None) -> None:
        self._cwd = Path(working_dir).resolve()
        self._history = history

    @property
    def name(self) -> str:
        return "edit_file"

    @property
    def description(self) -> str:
        return (
            "Edit a file by replacing exact text. The old_string must match exactly "
            "one location. Include enough context (3+ surrounding lines) to be unique."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path relative to the working directory."},
                "old_string": {"type": "string", "description": "Exact text to find (must appear exactly once)."},
                "new_string": {"type": "string", "description": "Replacement text."},
                "preview": {"type": "boolean", "description": "If true, return diff without applying. Default: false."},
            },
            "required": ["path", "old_string", "new_string"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        path = _resolve(self._cwd, kwargs["path"])
        try:
            path.relative_to(self._cwd)
        except ValueError:
            return ToolResult(error="Cannot edit files outside the working directory.", success=False)
        if not path.is_file():
            return ToolResult(error=f"File not found: {kwargs['path']}", success=False)

        old_string = kwargs["old_string"]
        new_string = kwargs["new_string"]
        preview = kwargs.get("preview", False)

        text = path.read_text(encoding="utf-8")
        count = text.count(old_string)

        if count == 0:
            return ToolResult(error="old_string not found in file.", success=False)
        if count > 1:
            return ToolResult(
                error=f"old_string matches {count} locations. Add more context to be unique.",
                success=False,
            )

        new_text = text.replace(old_string, new_string, 1)

        # Generate unified diff
        diff = difflib.unified_diff(
            text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f"a/{kwargs['path']}",
            tofile=f"b/{kwargs['path']}",
        )
        diff_str = "".join(diff)

        if preview:
            return ToolResult(output=diff_str or "(no changes)")

        # Record undo snapshot before mutation
        if self._history:
            rel = str(path.relative_to(self._cwd))
            self._history.record(rel, text)

        path.write_text(new_text, encoding="utf-8")
        return ToolResult(output=f"Applied edit to {kwargs['path']}\n\n{diff_str}")
