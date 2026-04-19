# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/tokens.py:200
# Component id: qk.source.ass_ade.update_from_usage
__version__ = "0.1.0"

    def update_from_usage(self, usage: dict[str, int] | None) -> None:
        """Update running totals from a completion response's usage dict."""
        if not usage:
            return
        self.prompt_tokens = usage.get("prompt_tokens", self.prompt_tokens)
        self.completion_tokens += usage.get("completion_tokens", 0)
        self.total_calls += 1
