# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testcataloginvariants.py:28
# Component id: qk.source.a0_qk_constants.test_local_providers_have_no_api_key_env
from __future__ import annotations

__version__ = "0.1.0"

def test_local_providers_have_no_api_key_env(self):
    for name, profile in FREE_PROVIDERS.items():
        if profile.local:
            assert profile.api_key_env is None, f"{name} is local but has api_key_env"
