# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_tcaengine.py:45
# Component id: mo.source.ass_ade.record_read
__version__ = "0.1.0"

    def record_read(self, path: str | Path) -> None:
        """Mark a file as freshly read. Call this from MCP read_file handler."""
        key = str(Path(path).resolve())
        self._reads[key] = time.time()
        self._save_state()
