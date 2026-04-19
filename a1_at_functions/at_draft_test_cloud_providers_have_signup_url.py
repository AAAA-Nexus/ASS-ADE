# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_cloud_providers_have_signup_url.py:7
# Component id: at.source.a1_at_functions.test_cloud_providers_have_signup_url
from __future__ import annotations

__version__ = "0.1.0"

def test_cloud_providers_have_signup_url(self):
    exempt = {"pollinations"}  # no signup needed
    for name, profile in FREE_PROVIDERS.items():
        if not profile.local and name not in exempt:
            assert profile.signup_url, f"{name} is cloud without signup_url"
