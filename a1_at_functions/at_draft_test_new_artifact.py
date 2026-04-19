# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_new_artifact.py:7
# Component id: at.source.a1_at_functions.test_new_artifact
from __future__ import annotations

__version__ = "0.1.0"

def test_new_artifact(self):
    version, change_type = assign_version("at.foo", "", "python", {})
    assert version == INITIAL_VERSION
    assert change_type == "new"
