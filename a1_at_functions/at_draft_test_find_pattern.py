# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testgrepsearch.py:8
# Component id: at.source.a2_mo_composites.test_find_pattern
from __future__ import annotations

__version__ = "0.1.0"

def test_find_pattern(self, workspace: Path):
    tool = GrepSearchTool(str(workspace))
    r = tool.execute(pattern="hello")
    assert r.success
    assert "hello.py" in r.output
