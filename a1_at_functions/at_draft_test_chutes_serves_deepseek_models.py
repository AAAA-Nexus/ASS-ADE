# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_chutes_serves_deepseek_models.py:7
# Component id: at.source.a1_at_functions.test_chutes_serves_deepseek_models
from __future__ import annotations

__version__ = "0.1.0"

def test_chutes_serves_deepseek_models(self):
    profile = get_provider("chutes")
    assert "deepseek" in profile.models_by_tier["balanced"].lower()
    assert "deepseek" in profile.models_by_tier["deep"].lower()
