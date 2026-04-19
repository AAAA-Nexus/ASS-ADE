# Extracted from C:/!ass-ade/src/ass_ade/agent/providers.py:443
# Component id: at.source.ass_ade.provider_for_model
from __future__ import annotations

__version__ = "0.1.0"

def provider_for_model(model: str) -> str | None:
    """Reverse-lookup: which provider serves this model id?

    Used by the MultiProvider to route a CompletionRequest.model back to the
    correct underlying OpenAICompatibleProvider instance.
    """
    if not model:
        return None
    for name, profile in FREE_PROVIDERS.items():
        for candidate in profile.models_by_tier.values():
            if candidate == model:
                return name
    return None
