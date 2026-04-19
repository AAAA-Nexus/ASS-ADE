# Extracted from C:/!ass-ade/tests/test_free_providers.py:641
# Component id: at.source.ass_ade.test_chutes_serves_deepseek_models
from __future__ import annotations

__version__ = "0.1.0"

def test_chutes_serves_deepseek_models(self):
    profile = get_provider("chutes")
    assert "deepseek" in profile.models_by_tier["balanced"].lower()
    assert "deepseek" in profile.models_by_tier["deep"].lower()
