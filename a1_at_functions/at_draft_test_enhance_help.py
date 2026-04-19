# Extracted from C:/!ass-ade/tests/test_enhance_cli.py:29
# Component id: at.source.ass_ade.test_enhance_help
from __future__ import annotations

__version__ = "0.1.0"

def test_enhance_help() -> None:
    result = runner.invoke(app, ["enhance", "--help"])

    assert result.exit_code == 0
    assert "enhance" in result.output.lower()
