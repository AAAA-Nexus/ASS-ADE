# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_searchfilestool.py:29
# Component id: at.source.ass_ade.execute
__version__ = "0.1.0"

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
