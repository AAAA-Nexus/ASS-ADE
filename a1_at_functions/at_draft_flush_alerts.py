# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_bas.py:174
# Component id: at.source.ass_ade.flush_alerts
__version__ = "0.1.0"

    def flush_alerts(self) -> list[Alert]:
        """Drain and return the unflushed alerts buffer."""
        drained = list(self._unflushed)
        self._unflushed.clear()
        return drained
