# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/tokens.py:194
# Component id: qk.source.ass_ade.utilization
__version__ = "0.1.0"

    def utilization(self) -> float:
        """Fraction of context window currently used (0.0 – 1.0)."""
        if self.context_window == 0:
            return 1.0
        return min(1.0, self.prompt_tokens / self.context_window)
