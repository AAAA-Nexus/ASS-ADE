# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testreadfile.py:7
# Component id: mo.source.a2_mo_composites.testreadfile
from __future__ import annotations

__version__ = "0.1.0"

class TestReadFile:
    def test_read_full(self, workspace: Path):
        tool = ReadFileTool(str(workspace))
        r = tool.execute(path="hello.py")
        assert r.success
        assert "hello world" in r.output

    def test_read_line_range(self, workspace: Path):
        tool = ReadFileTool(str(workspace))
        r = tool.execute(path="sub/data.txt", start_line=2, end_line=2)
        assert r.success
        assert r.output.strip() == "line2"

    def test_read_missing(self, workspace: Path):
        tool = ReadFileTool(str(workspace))
        r = tool.execute(path="nope.py")
        assert not r.success
        assert "not found" in (r.error or "").lower()
