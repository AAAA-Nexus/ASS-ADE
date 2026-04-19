# Extracted from C:/!ass-ade/tests/test_protocol.py:141
# Component id: at.source.ass_ade.test_protocol_evolution_record_cli
from __future__ import annotations

__version__ = "0.1.0"

def test_protocol_evolution_record_cli(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "protocol",
            "evolution-record",
            "iteration",
            "--summary",
            "CLI event",
            "--path",
            str(tmp_path),
            "--command",
            "status=passed::python -m pytest tests/ -q --no-header",
            "--metric",
            "tests=1",
        ],
    )

    assert result.exit_code == 0
    assert "Evolution Event Recorded" in result.stdout
    assert (tmp_path / ".ass-ade" / "evolution" / "ledger.jsonl").exists()
