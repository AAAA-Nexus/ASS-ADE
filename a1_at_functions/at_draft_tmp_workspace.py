# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_history.py:13
# Component id: at.source.ass_ade.tmp_workspace
__version__ = "0.1.0"

def tmp_workspace(tmp_path: Path) -> Path:
    """Create a temporary workspace with a sample file."""
    sample = tmp_path / "hello.py"
    sample.write_text("print('hello')\n", encoding="utf-8")
    return tmp_path
