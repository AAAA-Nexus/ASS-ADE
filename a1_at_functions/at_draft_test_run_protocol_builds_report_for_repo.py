# Extracted from C:/!ass-ade/tests/test_protocol.py:17
# Component id: at.source.ass_ade.test_run_protocol_builds_report_for_repo
from __future__ import annotations

__version__ = "0.1.0"

def test_run_protocol_builds_report_for_repo(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "architecture.md").write_text("x", encoding="utf-8")
    (tmp_path / "docs" / "dev-stack.md").write_text("x", encoding="utf-8")
    (tmp_path / "docs" / "protocol.md").write_text("x", encoding="utf-8")
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github" / "copilot-instructions.md").write_text("x", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "ass_ade").mkdir()
    (tmp_path / "src" / "ass_ade" / "cli.py").write_text("x", encoding="utf-8")
    (tmp_path / "src" / "ass_ade" / "nexus").mkdir(parents=True)
    (tmp_path / "src" / "ass_ade" / "nexus" / "models.py").write_text("x", encoding="utf-8")
    (tmp_path / "src" / "ass_ade" / "local").mkdir(parents=True)
    (tmp_path / "src" / "ass_ade" / "local" / "repo.py").write_text("x", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_cli.py").write_text("x", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")

    report = run_protocol("Improve public shell", tmp_path, AssAdeConfig(profile="local"))

    assert report.goal == "Improve public shell"
    assert report.assessment.profile == "local"
    assert len(report.audit) == 5
    assert report.summary.startswith("Completed a public-safe enhancement cycle")
