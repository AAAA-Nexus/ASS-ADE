# Extracted from C:/!ass-ade/tests/test_free_providers.py:166
# Component id: at.source.ass_ade.test_provider_for_model_reverse_lookup
from __future__ import annotations

__version__ = "0.1.0"

def test_provider_for_model_reverse_lookup(self):
    # groq's balanced tier model
    groq_balanced = get_provider("groq").models_by_tier["balanced"]
    assert provider_for_model(groq_balanced) == "groq"
