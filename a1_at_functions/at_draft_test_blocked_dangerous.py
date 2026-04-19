# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_blocked_dangerous.py:7
# Component id: at.source.a1_at_functions.test_blocked_dangerous
from __future__ import annotations

__version__ = "0.1.0"

def test_blocked_dangerous(self, workspace: Path):
    tool = RunCommandTool(str(workspace))
    r = tool.execute(command="rm -rf /")
    assert not r.success
    assert "blocked" in (r.error or "").lower()
