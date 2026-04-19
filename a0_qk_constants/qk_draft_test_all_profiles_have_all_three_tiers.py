# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testcataloginvariants.py:18
# Component id: qk.source.a0_qk_constants.test_all_profiles_have_all_three_tiers
from __future__ import annotations

__version__ = "0.1.0"

def test_all_profiles_have_all_three_tiers(self):
    for name, profile in FREE_PROVIDERS.items():
        for tier in ALL_TIERS:
            assert tier in profile.models_by_tier, f"{name} missing {tier} tier"
            assert profile.models_by_tier[tier], f"{name} {tier} is empty"
