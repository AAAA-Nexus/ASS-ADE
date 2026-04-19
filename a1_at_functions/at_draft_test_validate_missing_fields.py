# Extracted from C:/!ass-ade/tests/test_a2a_cli.py:56
# Component id: at.source.ass_ade.test_validate_missing_fields
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_missing_fields(self, tmp_path: Path) -> None:
    card_file = tmp_path / "bad.json"
    card_file.write_text(json.dumps({"description": "Missing name"}), encoding="utf-8")

    result = runner.invoke(app, ["a2a", "validate", str(card_file)])
    assert result.exit_code == 1
