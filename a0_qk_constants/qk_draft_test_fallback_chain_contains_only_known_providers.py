# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testcataloginvariants.py:39
# Component id: qk.source.a0_qk_constants.test_fallback_chain_contains_only_known_providers
from __future__ import annotations

__version__ = "0.1.0"

def test_fallback_chain_contains_only_known_providers(self):
    known = set(FREE_PROVIDERS.keys())
    for name in DEFAULT_FALLBACK_CHAIN:
        assert name in known, f"fallback chain references unknown provider {name}"
