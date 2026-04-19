# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_repo_summary_counts_files_and_skips_ignored_dirs.py:5
# Component id: at.source.ass_ade.test_repo_summary_counts_files_and_skips_ignored_dirs
__version__ = "0.1.0"

def test_repo_summary_counts_files_and_skips_ignored_dirs(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / ".venv").mkdir()
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    (tmp_path / "src" / "main.py").write_text("print('ok')", encoding="utf-8")
    (tmp_path / ".venv" / "secret.py").write_text("ignored", encoding="utf-8")

    summary = summarize_repo(tmp_path)

    assert summary.total_files == 2
    assert summary.file_types["md"] == 1
    assert summary.file_types["py"] == 1
