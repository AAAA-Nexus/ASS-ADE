# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_local_card_displays.py:7
# Component id: at.source.a1_at_functions.test_local_card_displays
from __future__ import annotations

__version__ = "0.1.0"

def test_local_card_displays(self) -> None:
    result = runner.invoke(app, ["a2a", "local-card"])
    assert result.exit_code == 0
    assert "ASS-ADE" in result.stdout
