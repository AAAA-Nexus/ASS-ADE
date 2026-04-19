# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testwritefile.py:7
# Component id: mo.source.a2_mo_composites.testwritefile
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
