# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:107
# Component id: at.source.ass_ade.test_echo
from __future__ import annotations

__version__ = "0.1.0"

def test_echo(self, workspace: Path):
    tool = RunCommandTool(str(workspace))
    r = tool.execute(command='python -c "print(\'hello\')"')
    assert r.success
    assert "hello" in r.output
