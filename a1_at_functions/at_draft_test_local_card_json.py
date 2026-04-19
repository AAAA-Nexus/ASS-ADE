# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_local_card_json.py:7
# Component id: at.source.a1_at_functions.test_local_card_json
from __future__ import annotations

__version__ = "0.1.0"

def test_local_card_json(self) -> None:
    result = runner.invoke(app, ["a2a", "local-card", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.stdout, strict=False)
    assert data["name"] == "ASS-ADE"
    assert "skills" in data
