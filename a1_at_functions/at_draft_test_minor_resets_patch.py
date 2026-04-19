# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_minor_resets_patch.py:7
# Component id: at.source.a1_at_functions.test_minor_resets_patch
from __future__ import annotations

__version__ = "0.1.0"

def test_minor_resets_patch(self):
    assert bump_version("1.2.9", "minor") == "1.3.0"
