# Extracted from C:/!ass-ade/tests/test_history.py:58
# Component id: at.source.ass_ade.test_undo_no_history
from __future__ import annotations

__version__ = "0.1.0"

def test_undo_no_history(self, history: FileHistory):
    assert history.undo("nonexistent.py") is None
