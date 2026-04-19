# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_epistemicrouter.py:45
# Component id: sy.source.ass_ade.avg_complexity
__version__ = "0.1.0"

    def avg_complexity(self) -> float:
        """Average complexity across all routed messages."""
        if not self._history:
            return 0.0
        return sum(d.complexity for d in self._history) / len(self._history)
