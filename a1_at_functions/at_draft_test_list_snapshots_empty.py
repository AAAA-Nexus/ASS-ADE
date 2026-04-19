# Extracted from C:/!ass-ade/tests/test_history.py:78
# Component id: at.source.ass_ade.test_list_snapshots_empty
from __future__ import annotations

__version__ = "0.1.0"

def test_list_snapshots_empty(self, history: FileHistory):
    assert history.list_snapshots("nonexistent.py") == []
