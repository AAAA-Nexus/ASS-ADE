# Extracted from C:/!ass-ade/tests/test_enhance_cli.py:92
# Component id: at.source.ass_ade.test_enhance_nonexistent_path
from __future__ import annotations

__version__ = "0.1.0"

def test_enhance_nonexistent_path() -> None:
    result = runner.invoke(app, ["enhance", "/nonexistent/path/xyz"])

    assert result.exit_code == 1
