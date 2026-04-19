# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/tools/builtin.py:378
# Component id: mo.source.ass_ade.searchfilestool
__version__ = "0.1.0"

class SearchFilesTool:
    """Find files matching a glob pattern."""

    def __init__(self, working_dir: str = ".") -> None:
        self._cwd = Path(working_dir).resolve()

    @property
    def name(self) -> str:
        return "search_files"

    @property
    def description(self) -> str:
        return "Find files matching a glob pattern (e.g., '**/*.py', 'src/**/*.ts')."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Glob pattern to match files."},
            },
            "required": ["pattern"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        pattern = kwargs["pattern"]
        matches = sorted(self._cwd.glob(pattern))

        filtered = [
            m
            for m in matches
            if m.is_file()
            and not any(p in _SKIP_DIRS for p in m.relative_to(self._cwd).parts)
        ]

        if not filtered:
            return ToolResult(output="No matches found.")

        lines = [str(m.relative_to(self._cwd)) for m in filtered[:_MAX_GLOB_RESULTS]]
        if len(filtered) > _MAX_GLOB_RESULTS:
            lines.append(f"... and {len(filtered) - _MAX_GLOB_RESULTS} more matches")

        return ToolResult(output="\n".join(lines))
