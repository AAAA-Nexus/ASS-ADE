# Extracted from C:/!ass-ade/tests/test_version_tracker.py:120
# Component id: at.source.ass_ade.test_new_artifact
from __future__ import annotations

__version__ = "0.1.0"

def test_new_artifact(self):
    version, change_type = assign_version("at.foo", "", "python", {})
    assert version == INITIAL_VERSION
    assert change_type == "new"
