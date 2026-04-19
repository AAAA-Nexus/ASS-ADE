# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli.py:269
# Component id: at.source.ass_ade.test_auto_detect_helper
__version__ = "0.1.0"

def test_auto_detect_helper(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "util.py").write_text("def f(): pass\n", encoding="utf-8")

    from ass_ade.cli import _auto_detect_project
    result = _auto_detect_project(tmp_path)

    assert "Python" in result
    assert "files" in result
    assert "Try:" in result
