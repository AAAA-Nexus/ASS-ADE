# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_read_full.py:7
# Component id: at.source.a1_at_functions.test_read_full
from __future__ import annotations

__version__ = "0.1.0"

def test_read_full(self, workspace: Path):
    tool = ReadFileTool(str(workspace))
    r = tool.execute(path="hello.py")
    assert r.success
    assert "hello world" in r.output
