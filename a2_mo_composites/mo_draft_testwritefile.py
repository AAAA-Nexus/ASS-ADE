# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:58
# Component id: mo.source.ass_ade.testwritefile
from __future__ import annotations

__version__ = "0.1.0"

class TestWriteFile:
    def test_create_new(self, workspace: Path):
        tool = WriteFileTool(str(workspace))
        r = tool.execute(path="new.py", content="x = 1\n")
        assert r.success
        assert (workspace / "new.py").read_text() == "x = 1\n"

    def test_create_nested(self, workspace: Path):
        tool = WriteFileTool(str(workspace))
        r = tool.execute(path="a/b/c.py", content="pass\n")
        assert r.success
        assert (workspace / "a" / "b" / "c.py").exists()

    def test_reject_outside_cwd(self, workspace: Path):
        tool = WriteFileTool(str(workspace))
        # Try to escape up
        r = tool.execute(path="../escape.py", content="pwned")
        assert not r.success
        assert "outside" in (r.error or "").lower()
