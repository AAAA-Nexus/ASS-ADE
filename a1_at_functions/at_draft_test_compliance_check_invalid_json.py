# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_compliance_check_invalid_json.py:7
# Component id: at.source.a1_at_functions.test_compliance_check_invalid_json
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
