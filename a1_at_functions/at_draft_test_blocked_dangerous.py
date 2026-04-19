# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:113
# Component id: at.source.ass_ade.test_blocked_dangerous
from __future__ import annotations

__version__ = "0.1.0"

def test_blocked_dangerous(self, workspace: Path):
    tool = RunCommandTool(str(workspace))
    r = tool.execute(command="rm -rf /")
    assert not r.success
    assert "blocked" in (r.error or "").lower()
