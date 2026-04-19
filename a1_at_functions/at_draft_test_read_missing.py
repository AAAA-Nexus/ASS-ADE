# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:48
# Component id: at.source.ass_ade.test_read_missing
from __future__ import annotations

__version__ = "0.1.0"

def test_read_missing(self, workspace: Path):
    tool = ReadFileTool(str(workspace))
    r = tool.execute(path="nope.py")
    assert not r.success
    assert "not found" in (r.error or "").lower()
