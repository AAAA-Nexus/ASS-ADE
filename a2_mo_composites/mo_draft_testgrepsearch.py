# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testgrepsearch.py:7
# Component id: mo.source.a2_mo_composites.testgrepsearch
from __future__ import annotations

__version__ = "0.1.0"

class TestGrepSearch:
    def test_find_pattern(self, workspace: Path):
        tool = GrepSearchTool(str(workspace))
        r = tool.execute(pattern="hello")
        assert r.success
        assert "hello.py" in r.output

    def test_no_matches(self, workspace: Path):
        tool = GrepSearchTool(str(workspace))
        r = tool.execute(pattern="ZZZZZ_NOTHING")
        assert "No matches" in r.output

    def test_invalid_regex(self, workspace: Path):
        tool = GrepSearchTool(str(workspace))
        r = tool.execute(pattern="[invalid")
        assert not r.success
        assert "Invalid regex" in (r.error or "")
