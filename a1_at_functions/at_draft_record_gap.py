# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/tca.py:125
# Component id: at.source.ass_ade.record_gap
__version__ = "0.1.0"

    def record_gap(self, description: str, source: str = "") -> None:
        """Record a documentation gap discovered during synthesis."""
        self._gaps.append(GAPEntry(description=description, source=source))
