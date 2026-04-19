# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testgrepsearch.py:19
# Component id: at.source.a2_mo_composites.test_invalid_regex
from __future__ import annotations

__version__ = "0.1.0"

def test_invalid_regex(self, workspace: Path):
    tool = GrepSearchTool(str(workspace))
    r = tool.execute(pattern="[invalid")
    assert not r.success
    assert "Invalid regex" in (r.error or "")
