# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:154
# Component id: at.source.ass_ade.test_no_matches
from __future__ import annotations

__version__ = "0.1.0"

def test_no_matches(self, workspace: Path):
    tool = SearchFilesTool(str(workspace))
    r = tool.execute(pattern="**/*.rs")
    assert "No matches" in r.output
