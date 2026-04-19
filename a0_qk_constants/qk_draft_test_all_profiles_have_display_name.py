# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testcataloginvariants.py:24
# Component id: qk.source.a0_qk_constants.test_all_profiles_have_display_name
from __future__ import annotations

__version__ = "0.1.0"

def test_all_profiles_have_display_name(self):
    for name, profile in FREE_PROVIDERS.items():
        assert profile.display_name, f"{name} has no display_name"
