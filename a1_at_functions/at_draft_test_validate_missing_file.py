# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testa2avalidatecli.py:29
# Component id: at.source.a1_at_functions.test_validate_missing_file
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_missing_file(self) -> None:
    result = runner.invoke(app, ["a2a", "validate", "/nonexistent/agent.json"])
    assert result.exit_code == 1
