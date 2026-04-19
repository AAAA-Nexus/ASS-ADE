# Extracted from C:/!ass-ade/src/ass_ade/tools/builtin.py:326
# Component id: mo.source.ass_ade.listdirectorytool
from __future__ import annotations

__version__ = "0.1.0"

class ListDirectoryTool:
    """List files and directories."""

    def __init__(self, working_dir: str = ".") -> None:
        self._cwd = Path(working_dir).resolve()

    @property
    def name(self) -> str:
        return "list_directory"

    @property
    def description(self) -> str:
        return "List files and directories. Entries ending with / are directories."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory path (default: working directory).",
                },
            },
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        path = _resolve(self._cwd, kwargs.get("path", "."))
        try:
            path.relative_to(self._cwd)
        except ValueError:
            return ToolResult(error="Cannot list directories outside the working directory.", success=False)
        if not path.is_dir():
            return ToolResult(error=f"Not a directory: {kwargs.get('path', '.')}", success=False)

        entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        lines: list[str] = []
        for entry in entries[:_MAX_DIR_ENTRIES]:
            suffix = "/" if entry.is_dir() else ""
            lines.append(f"{entry.name}{suffix}")

        if len(entries) > _MAX_DIR_ENTRIES:
            lines.append(f"... and {len(entries) - _MAX_DIR_ENTRIES} more entries")

        return ToolResult(output="\n".join(lines))
