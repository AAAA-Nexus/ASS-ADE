# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:36
# Component id: at.source.ass_ade.test_read_full
from __future__ import annotations

__version__ = "0.1.0"

def test_read_full(self, workspace: Path):
    tool = ReadFileTool(str(workspace))
    r = tool.execute(path="hello.py")
    assert r.success
    assert "hello world" in r.output
