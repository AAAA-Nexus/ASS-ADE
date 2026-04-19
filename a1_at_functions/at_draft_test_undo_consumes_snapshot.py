# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_undo_consumes_snapshot.py:7
# Component id: at.source.a1_at_functions.test_undo_consumes_snapshot
from __future__ import annotations

__version__ = "0.1.0"

def test_undo_consumes_snapshot(self, history: FileHistory, tmp_workspace: Path):
    history.record("hello.py", "v1")
    history.record("hello.py", "v2")
    assert history.depth("hello.py") == 2

    history.undo("hello.py")
    assert history.depth("hello.py") == 1
