# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:119
# Component id: at.source.ass_ade.test_timeout
from __future__ import annotations

__version__ = "0.1.0"

def test_timeout(self, workspace: Path):
    tool = RunCommandTool(str(workspace))
    r = tool.execute(command="python -c \"import time; time.sleep(10)\"", timeout=1)
    assert not r.success
    assert "timed out" in (r.error or "").lower()
