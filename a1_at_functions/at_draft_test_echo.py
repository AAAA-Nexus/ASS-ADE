# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_echo.py:7
# Component id: at.source.a1_at_functions.test_echo
from __future__ import annotations

__version__ = "0.1.0"

def test_echo(self, workspace: Path):
    tool = RunCommandTool(str(workspace))
    r = tool.execute(command='python -c "print(\'hello\')"')
    assert r.success
    assert "hello" in r.output
