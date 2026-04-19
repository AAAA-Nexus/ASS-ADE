# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/tokens.py:185
# Component id: qk.source.ass_ade.for_model
__version__ = "0.1.0"

    def for_model(cls, model: str | None) -> TokenBudget:
        return cls(context_window=context_window_for(model))
