# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testruncommand.py:7
# Component id: mo.source.a2_mo_composites.testruncommand
from __future__ import annotations

__version__ = "0.1.0"

class TestRunCommand:
    def test_echo(self, workspace: Path):
        tool = RunCommandTool(str(workspace))
        r = tool.execute(command='python -c "print(\'hello\')"')
        assert r.success
        assert "hello" in r.output

    def test_blocked_dangerous(self, workspace: Path):
        tool = RunCommandTool(str(workspace))
        r = tool.execute(command="rm -rf /")
        assert not r.success
        assert "blocked" in (r.error or "").lower()

    def test_timeout(self, workspace: Path):
        tool = RunCommandTool(str(workspace))
        r = tool.execute(command="python -c \"import time; time.sleep(10)\"", timeout=1)
        assert not r.success
        assert "timed out" in (r.error or "").lower()
