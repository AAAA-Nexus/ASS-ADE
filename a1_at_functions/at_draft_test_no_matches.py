# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testgrepsearch.py:14
# Component id: at.source.a2_mo_composites.test_no_matches
from __future__ import annotations

__version__ = "0.1.0"

def test_no_matches(self, workspace: Path):
    tool = GrepSearchTool(str(workspace))
    r = tool.execute(pattern="ZZZZZ_NOTHING")
    assert "No matches" in r.output
