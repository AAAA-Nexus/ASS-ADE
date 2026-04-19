# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_reject_outside_cwd.py:7
# Component id: at.source.a1_at_functions.test_reject_outside_cwd
from __future__ import annotations

__version__ = "0.1.0"

def test_reject_outside_cwd(self, workspace: Path):
    tool = WriteFileTool(str(workspace))
    # Try to escape up
    r = tool.execute(path="../escape.py", content="pwned")
    assert not r.success
    assert "outside" in (r.error or "").lower()
