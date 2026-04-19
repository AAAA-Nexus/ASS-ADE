# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_memorystore.py:58
# Component id: mo.source.ass_ade.clear
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
