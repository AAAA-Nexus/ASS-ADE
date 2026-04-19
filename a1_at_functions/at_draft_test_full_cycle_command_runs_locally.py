# Extracted from C:/!ass-ade/tests/test_cli.py:55
# Component id: at.source.ass_ade.test_full_cycle_command_runs_locally
from __future__ import annotations

__version__ = "0.1.0"

def test_full_cycle_command_runs_locally(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")

    result = runner.invoke(app, ["cycle", "Enhance via cycle", "--path", str(tmp_path)])

    assert result.exit_code == 0
    assert "ASS-ADE Full Cycle" in result.stdout
    assert "Protocol Summary" in result.stdout
