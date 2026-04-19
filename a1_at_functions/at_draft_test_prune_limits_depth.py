# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_prune_limits_depth.py:7
# Component id: at.source.a1_at_functions.test_prune_limits_depth
from __future__ import annotations

__version__ = "0.1.0"

def test_prune_limits_depth(self, history: FileHistory):
    for i in range(10):
        history.record("hello.py", f"version {i}")

    # max_depth is 5
    assert history.depth("hello.py") == 5

    # Should keep the latest 5
    snaps = history.list_snapshots("hello.py")
    assert snaps[0].content == "version 5"
    assert snaps[-1].content == "version 9"
