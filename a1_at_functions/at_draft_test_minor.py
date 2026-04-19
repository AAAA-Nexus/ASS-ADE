# Extracted from C:/!ass-ade/tests/test_version_tracker.py:30
# Component id: at.source.ass_ade.test_minor
from __future__ import annotations

__version__ = "0.1.0"

def test_minor(self):
    assert bump_version("0.1.3", "minor") == "0.2.0"
