# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/routing.py:221
# Component id: at.source.ass_ade.avg_complexity
__version__ = "0.1.0"

    def avg_complexity(self) -> float:
        """Average complexity across all routed messages."""
        if not self._history:
            return 0.0
        return sum(d.complexity for d in self._history) / len(self._history)
