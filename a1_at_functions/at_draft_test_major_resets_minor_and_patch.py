# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_major_resets_minor_and_patch.py:7
# Component id: at.source.a1_at_functions.test_major_resets_minor_and_patch
from __future__ import annotations

__version__ = "0.1.0"

def test_major_resets_minor_and_patch(self):
    assert bump_version("2.5.7", "major") == "3.0.0"
