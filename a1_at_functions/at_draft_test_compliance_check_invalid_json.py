# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:727
# Component id: at.source.ass_ade.test_compliance_check_invalid_json
from __future__ import annotations

__version__ = "0.1.0"

def test_compliance_check_invalid_json(self, tmp_path: Path, hybrid_config: Path) -> None:
    """Compliance check should error if payload is invalid JSON."""
    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{ invalid json }", encoding="utf-8")

    result = runner.invoke(
        app,
        ["compliance", "check", str(bad_json), "--config", str(hybrid_config)],
    )

    assert result.exit_code != 0
