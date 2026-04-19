# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/tools/builtin.py:49
# Component id: mo.source.ass_ade.readfiletool
__version__ = "0.1.0"

class ReadFileTool:
    """Read file contents, optionally a specific line range."""

    def __init__(self, working_dir: str = ".") -> None:
        self._cwd = Path(working_dir).resolve()

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Read the contents of a file. Use start_line/end_line for partial reads (1-based, inclusive)."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path relative to the working directory."},
                "start_line": {"type": "integer", "description": "First line to read (1-based). Omit for full file."},
                "end_line": {"type": "integer", "description": "Last line to read (1-based, inclusive)."},
            },
            "required": ["path"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        path = _resolve(self._cwd, kwargs["path"])
        try:
            path.relative_to(self._cwd)
        except ValueError:
            return ToolResult(error="Cannot read files outside the working directory.", success=False)
        if not path.is_file():
            return ToolResult(error=f"File not found: {kwargs['path']}", success=False)

        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines(keepends=True)

        start = kwargs.get("start_line")
        end = kwargs.get("end_line")
        if start is not None:
            start = max(1, int(start)) - 1
            end = int(end) if end else len(lines)
            lines = lines[start:end]

        content = "".join(lines)
        if len(content) > _MAX_FILE_OUTPUT:
            content = content[:_MAX_FILE_OUTPUT] + "\n... [truncated at 100KB]"
        return ToolResult(output=content)
