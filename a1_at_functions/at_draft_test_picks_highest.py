# Extracted from C:/!ass-ade/tests/test_version_tracker.py:184
# Component id: at.source.ass_ade.test_picks_highest
from __future__ import annotations

__version__ = "0.1.0"

def test_picks_highest(self):
    assert _aggregate_version(["0.1.0", "0.2.0", "0.1.5"]) == "0.2.0"
