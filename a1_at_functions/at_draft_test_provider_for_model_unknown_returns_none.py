# Extracted from C:/!ass-ade/tests/test_free_providers.py:171
# Component id: at.source.ass_ade.test_provider_for_model_unknown_returns_none
from __future__ import annotations

__version__ = "0.1.0"

def test_provider_for_model_unknown_returns_none(self):
    assert provider_for_model("not-a-real-model") is None
