from pathlib import Path

from ass_ade.local.repo import summarize_repo


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
