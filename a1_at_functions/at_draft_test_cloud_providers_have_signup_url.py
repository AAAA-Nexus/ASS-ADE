# Extracted from C:/!ass-ade/tests/test_free_providers.py:59
# Component id: at.source.ass_ade.test_cloud_providers_have_signup_url
from __future__ import annotations

__version__ = "0.1.0"

def test_cloud_providers_have_signup_url(self):
    exempt = {"pollinations"}  # no signup needed
    for name, profile in FREE_PROVIDERS.items():
        if not profile.local and name not in exempt:
            assert profile.signup_url, f"{name} is cloud without signup_url"
