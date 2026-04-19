# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testa2avalidatecli.py:22
# Component id: at.source.a1_at_functions.test_validate_missing_fields
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_missing_fields(self, tmp_path: Path) -> None:
    card_file = tmp_path / "bad.json"
    card_file.write_text(json.dumps({"description": "Missing name"}), encoding="utf-8")

    result = runner.invoke(app, ["a2a", "validate", str(card_file)])
    assert result.exit_code == 1
