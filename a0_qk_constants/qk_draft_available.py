# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/tokens.py:189
# Component id: qk.source.ass_ade.available
__version__ = "0.1.0"

    def available(self) -> int:
        """Tokens available for prompt content (messages + tools)."""
        return max(0, self.context_window - self.reserve)
