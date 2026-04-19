# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testregistry.py:19
# Component id: og.source.a3_og_features.test_execute_unknown
from __future__ import annotations

__version__ = "0.1.0"

def test_execute_unknown(self, workspace: Path):
    reg = default_registry(str(workspace))
    r = reg.execute("no_such_tool")
    assert not r.success
    assert "Unknown tool" in (r.error or "")
