# Extracted from C:/!ass-ade/tests/test_version_tracker.py:187
# Component id: at.source.ass_ade.test_empty_list_returns_initial
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_list_returns_initial(self):
    assert _aggregate_version([]) == INITIAL_VERSION
