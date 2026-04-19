# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_run_linters_returns_dict.py:5
# Component id: at.source.ass_ade.test_run_linters_returns_dict
__version__ = "0.1.0"

def test_run_linters_returns_dict(tmp_path: Path) -> None:
    (tmp_path / "hello.py").write_text("x = 1\n", encoding="utf-8")

    result = run_linters(tmp_path)

    assert isinstance(result, dict)
    assert "root" in result
    assert "linters_run" in result
    assert "results" in result
