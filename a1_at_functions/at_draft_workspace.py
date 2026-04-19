# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_plan.py:14
# Component id: at.source.ass_ade.workspace
__version__ = "0.1.0"

def workspace(tmp_path: Path) -> Path:
    (tmp_path / "main.py").write_text("def main():\n    pass\n", encoding="utf-8")
    (tmp_path / "utils.py").write_text("def helper():\n    return 42\n", encoding="utf-8")
    return tmp_path
