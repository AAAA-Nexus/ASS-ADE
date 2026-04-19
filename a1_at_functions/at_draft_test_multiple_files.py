# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_multiple_files.py:7
# Component id: at.source.a1_at_functions.test_multiple_files
from __future__ import annotations

__version__ = "0.1.0"

def test_multiple_files(self, history: FileHistory, tmp_workspace: Path):
    (tmp_workspace / "other.py").write_text("other", encoding="utf-8")
    history.record("hello.py", "h1")
    history.record("other.py", "o1")

    assert history.depth("hello.py") == 1
    assert history.depth("other.py") == 1
