# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_lint_nonexistent_path.py:7
# Component id: at.source.a1_at_functions.test_lint_nonexistent_path
from __future__ import annotations

__version__ = "0.1.0"

def test_lint_nonexistent_path() -> None:
    result = runner.invoke(app, ["lint", "/nonexistent/path/that/does/not/exist"])

    assert result.exit_code == 1
