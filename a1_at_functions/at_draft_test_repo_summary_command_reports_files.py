# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_repo_summary_command_reports_files.py:7
# Component id: at.source.a1_at_functions.test_repo_summary_command_reports_files
from __future__ import annotations

__version__ = "0.1.0"

def test_repo_summary_command_reports_files(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("pass", encoding="utf-8")

    result = runner.invoke(app, ["repo", "summary", str(tmp_path)])

    assert result.exit_code == 0
    assert "Repo Summary" in result.stdout
    assert "Top File Types" in result.stdout
