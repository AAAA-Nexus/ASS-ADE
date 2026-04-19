# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_history.py:21
# Component id: at.source.ass_ade.history
__version__ = "0.1.0"

def history(tmp_workspace: Path) -> FileHistory:
    return FileHistory(str(tmp_workspace), max_depth=5)
