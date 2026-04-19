# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_grepsearchtool.py:7
# Component id: mo.source.a2_mo_composites.grepsearchtool
from __future__ import annotations

__version__ = "0.1.0"

class GrepSearchTool:
    """Search file contents by regex pattern."""

    def __init__(self, working_dir: str = ".") -> None:
        self._cwd = Path(working_dir).resolve()

    @property
    def name(self) -> str:
        return "grep_search"

    @property
    def description(self) -> str:
        return "Search file contents for a regex pattern. Returns matching lines with file:line: prefix."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Regex pattern (case-insensitive)."},
                "include": {
                    "type": "string",
                    "description": "Glob to filter files (e.g., '**/*.py'). Default: all files.",
                },
            },
            "required": ["pattern"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        pattern_str = kwargs["pattern"]
        include = kwargs.get("include", "**/*")

        try:
            pattern = re.compile(pattern_str, re.IGNORECASE)
        except re.error as exc:
            return ToolResult(error=f"Invalid regex: {exc}", success=False)

        results: list[str] = []
        for filepath in sorted(self._cwd.glob(include)):
            if not filepath.is_file():
                continue
            parts = filepath.relative_to(self._cwd).parts
            if any(p in _SKIP_DIRS for p in parts):
                continue

            try:
                text = filepath.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue

            rel = str(filepath.relative_to(self._cwd))
            for i, line in enumerate(text.splitlines(), 1):
                if pattern.search(line):
                    results.append(f"{rel}:{i}: {line.rstrip()}")
                    if len(results) >= _MAX_GREP_MATCHES:
                        results.append("... [truncated at 100 matches]")
                        return ToolResult(output="\n".join(results))

        if not results:
            return ToolResult(output="No matches found.")
        return ToolResult(output="\n".join(results))
