# Extracted from C:/!ass-ade/tests/test_version_tracker.py:200
# Component id: at.source.ass_ade.test_none_path_returns_empty
from __future__ import annotations

__version__ = "0.1.0"

def test_none_path_returns_empty(self):
    assert load_prev_versions(None) == {}
