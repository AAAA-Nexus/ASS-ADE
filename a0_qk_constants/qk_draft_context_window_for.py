# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/tokens.py:141
# Component id: qk.source.ass_ade.context_window_for
__version__ = "0.1.0"

def context_window_for(model: str | None) -> int:
    """Look up the context window for a model name.

    Performs fuzzy matching: if the exact name isn't in the table,
    checks if any key is a substring of the model name (handles
    provider-prefixed names like 'ollama/llama-3.1-8b').
    """
    if not model:
        return DEFAULT_CONTEXT_WINDOW

    low = model.lower()
    if low in _CONTEXT_WINDOWS:
        return _CONTEXT_WINDOWS[low]

    for key, val in _CONTEXT_WINDOWS.items():
        if key in low or low in key:
            return val

    return DEFAULT_CONTEXT_WINDOW
