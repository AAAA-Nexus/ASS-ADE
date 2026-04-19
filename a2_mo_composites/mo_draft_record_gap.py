# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_tcaengine.py:88
# Component id: mo.source.ass_ade.record_gap
__version__ = "0.1.0"

    def record_gap(self, description: str, source: str = "") -> None:
        """Record a documentation gap discovered during synthesis."""
        self._gaps.append(GAPEntry(description=description, source=source))
