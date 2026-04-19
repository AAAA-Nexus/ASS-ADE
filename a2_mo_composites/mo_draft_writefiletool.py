# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_writefiletool.py:7
# Component id: mo.source.a2_mo_composites.writefiletool
from __future__ import annotations

__version__ = "0.1.0"

class WriteFileTool:
    """Create a new file or overwrite an existing file."""

    def __init__(self, working_dir: str = ".", history: FileHistory | None = None) -> None:
        self._cwd = Path(working_dir).resolve()
        self._history = history

    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "Create a new file or overwrite an existing file with the given content."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path relative to the working directory."},
                "content": {"type": "string", "description": "Full content to write."},
            },
            "required": ["path", "content"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        path = _resolve(self._cwd, kwargs["path"])
        content = kwargs["content"]

        try:
            path.relative_to(self._cwd)
        except ValueError:
            return ToolResult(error="Cannot write outside the working directory.", success=False)

        # Record undo snapshot if file exists
        if path.is_file() and self._history:
            rel = str(path.relative_to(self._cwd))
            self._history.record(rel, path.read_text(encoding="utf-8"))

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return ToolResult(output=f"Wrote {len(content)} bytes to {kwargs['path']}")
