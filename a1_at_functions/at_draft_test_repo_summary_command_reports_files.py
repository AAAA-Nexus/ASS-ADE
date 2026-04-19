# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli.py:33
# Component id: at.source.ass_ade.test_repo_summary_command_reports_files
__version__ = "0.1.0"

def test_repo_summary_command_reports_files(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("pass", encoding="utf-8")

    result = runner.invoke(app, ["repo", "summary", str(tmp_path)])

    assert result.exit_code == 0
    assert "Repo Summary" in result.stdout
    assert "Top File Types" in result.stdout
