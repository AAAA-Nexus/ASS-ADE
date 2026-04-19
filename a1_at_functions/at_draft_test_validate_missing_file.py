# Extracted from C:/!ass-ade/tests/test_a2a_cli.py:63
# Component id: at.source.ass_ade.test_validate_missing_file
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_missing_file(self) -> None:
    result = runner.invoke(app, ["a2a", "validate", "/nonexistent/agent.json"])
    assert result.exit_code == 1
