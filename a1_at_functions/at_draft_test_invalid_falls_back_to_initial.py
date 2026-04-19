# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_invalid_falls_back_to_initial.py:7
# Component id: at.source.a1_at_functions.test_invalid_falls_back_to_initial
from __future__ import annotations

__version__ = "0.1.0"

def test_invalid_falls_back_to_initial(self):
    assert bump_version("not-semver", "patch") == INITIAL_VERSION
