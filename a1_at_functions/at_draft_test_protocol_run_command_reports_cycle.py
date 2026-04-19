# Extracted from C:/!ass-ade/tests/test_cli.py:45
# Component id: at.source.ass_ade.test_protocol_run_command_reports_cycle
from __future__ import annotations

__version__ = "0.1.0"

def test_protocol_run_command_reports_cycle(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")

    result = runner.invoke(app, ["protocol", "run", "Improve the public shell", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "ASS-ADE Protocol Report" in result.stdout
    assert "Audit" in result.stdout
