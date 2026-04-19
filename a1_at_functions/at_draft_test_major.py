# Extracted from C:/!ass-ade/tests/test_version_tracker.py:33
# Component id: at.source.ass_ade.test_major
from __future__ import annotations

__version__ = "0.1.0"

def test_major(self):
    assert bump_version("0.1.3", "major") == "1.0.0"
