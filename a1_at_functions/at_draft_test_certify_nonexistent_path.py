# Extracted from C:/!ass-ade/tests/test_new_codebase_commands.py:118
# Component id: at.source.ass_ade.test_certify_nonexistent_path
from __future__ import annotations

__version__ = "0.1.0"

def test_certify_nonexistent_path() -> None:
    result = runner.invoke(app, ["certify", "/nonexistent/path/that/does/not/exist"])

    assert result.exit_code == 1
