# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_wisdomengine.py:146
# Component id: mo.source.ass_ade.update_principles
__version__ = "0.1.0"

    def update_principles(self, principles: list[str]) -> list[str]:
        for p in principles:
            if p not in self._principles:
                self._principles.append(p)
