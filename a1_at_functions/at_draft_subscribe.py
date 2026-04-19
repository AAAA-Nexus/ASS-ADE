# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_bas.py:48
# Component id: at.source.ass_ade.subscribe
__version__ = "0.1.0"

    def subscribe(self, callback: Callable[[Alert], None]) -> None:
        self._subscribers.append(callback)
