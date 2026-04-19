# Extracted from C:/!ass-ade/tests/test_version_tracker.py:36
# Component id: at.source.ass_ade.test_invalid_falls_back_to_initial
from __future__ import annotations

__version__ = "0.1.0"

def test_invalid_falls_back_to_initial(self):
    assert bump_version("not-semver", "patch") == INITIAL_VERSION
