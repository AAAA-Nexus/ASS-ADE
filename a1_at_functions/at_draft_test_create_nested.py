# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:65
# Component id: at.source.ass_ade.test_create_nested
from __future__ import annotations

__version__ = "0.1.0"

def test_create_nested(self, workspace: Path):
    tool = WriteFileTool(str(workspace))
    r = tool.execute(path="a/b/c.py", content="pass\n")
    assert r.success
    assert (workspace / "a" / "b" / "c.py").exists()
