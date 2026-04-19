# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_provider_for_model_reverse_lookup.py:7
# Component id: at.source.a1_at_functions.test_provider_for_model_reverse_lookup
from __future__ import annotations

__version__ = "0.1.0"

def test_provider_for_model_reverse_lookup(self):
    # groq's balanced tier model
    groq_balanced = get_provider("groq").models_by_tier["balanced"]
    assert provider_for_model(groq_balanced) == "groq"
