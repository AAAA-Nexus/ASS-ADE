# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_protocol_run_command_reports_cycle.py:7
# Component id: at.source.a1_at_functions.test_protocol_run_command_reports_cycle
from __future__ import annotations

__version__ = "0.1.0"

def test_protocol_run_command_reports_cycle(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")

    result = runner.invoke(app, ["protocol", "run", "Improve the public shell", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "ASS-ADE Protocol Report" in result.stdout
    assert "Audit" in result.stdout
