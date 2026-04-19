# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testlistdirectory.py:7
# Component id: mo.source.a2_mo_composites.testlistdirectory
from __future__ import annotations

__version__ = "0.1.0"

class TestListDirectory:
    def test_list_root(self, workspace: Path):
        tool = ListDirectoryTool(str(workspace))
        r = tool.execute()
        assert r.success
        assert "hello.py" in r.output
        assert "sub/" in r.output

    def test_list_subdir(self, workspace: Path):
        tool = ListDirectoryTool(str(workspace))
        r = tool.execute(path="sub")
        assert r.success
        assert "data.txt" in r.output
