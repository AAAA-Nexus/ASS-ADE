# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_tcaengine.py:112
# Component id: mo.source.ass_ade.report
__version__ = "0.1.0"

    def report(self) -> dict[str, Any]:
        return {
            "engine": "tca",
            "tracked_files": len(self._reads),
            "stale_count": self._stale_count,
            "gap_count": len(self._gaps),
            "threshold_hours": self._threshold_hours,
        }
