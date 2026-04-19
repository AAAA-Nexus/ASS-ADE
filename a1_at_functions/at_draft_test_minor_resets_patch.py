# Extracted from C:/!ass-ade/tests/test_version_tracker.py:39
# Component id: at.source.ass_ade.test_minor_resets_patch
from __future__ import annotations

__version__ = "0.1.0"

def test_minor_resets_patch(self):
    assert bump_version("1.2.9", "minor") == "1.3.0"
