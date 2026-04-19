# Extracted from C:/!ass-ade/tests/test_free_providers.py:54
# Component id: at.source.ass_ade.test_local_providers_have_no_api_key_env
from __future__ import annotations

__version__ = "0.1.0"

def test_local_providers_have_no_api_key_env(self):
    for name, profile in FREE_PROVIDERS.items():
        if profile.local:
            assert profile.api_key_env is None, f"{name} is local but has api_key_env"
