# Extracted from C:/!ass-ade/tests/test_version_tracker.py:42
# Component id: at.source.ass_ade.test_major_resets_minor_and_patch
from __future__ import annotations

__version__ = "0.1.0"

def test_major_resets_minor_and_patch(self):
    assert bump_version("2.5.7", "major") == "3.0.0"
