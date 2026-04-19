# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_tcaengine.py:92
# Component id: mo.source.ass_ade.get_gaps
__version__ = "0.1.0"

    def get_gaps(self) -> list[dict[str, Any]]:
        return [
            {"description": g.description, "source": g.source, "ts": g.ts}
            for g in self._gaps
        ]
