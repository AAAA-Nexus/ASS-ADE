# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/interpreter.py:200
# Component id: at.source.ass_ade.clear
__version__ = "0.1.0"

    def clear(cls) -> None:
        for filename in [
            "user_profile.json", "project_contexts.json",
            "preferences.json", "conversation_history.jsonl",
        ]:
            p = _MEMORY_DIR / filename
            if p.exists():
                try:
                    p.unlink()
                except OSError:
                    pass
