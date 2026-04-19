# Extracted from C:/!ass-ade/tests/test_version_tracker.py:193
# Component id: at.source.ass_ade.test_major_wins
from __future__ import annotations

__version__ = "0.1.0"

def test_major_wins(self):
    assert _aggregate_version(["0.9.9", "1.0.0", "0.9.8"]) == "1.0.0"
