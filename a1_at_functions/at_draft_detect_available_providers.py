# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_detect_available_providers.py:7
# Component id: at.source.a1_at_functions.detect_available_providers
from __future__ import annotations

__version__ = "0.1.0"

def detect_available_providers(
    config_providers: dict[str, Any] | None = None,
) -> list[ProviderProfile]:
    """Return all providers with API keys available (env or config overrides).

    Local providers (ollama, lm studio) are always considered available even
    though they may not be running — the actual reachability check happens at
    request time, and a provider that 404s simply advances the fallback chain.
    """
    overrides = config_providers or {}
    available: list[ProviderProfile] = []
    for name, profile in FREE_PROVIDERS.items():
        user_override = overrides.get(name) if overrides else None
        user_key = None
        user_enabled = True
        if isinstance(user_override, dict):
            user_key = user_override.get("api_key")
            user_enabled = user_override.get("enabled", True)
        if not user_enabled:
            continue
        if profile.is_available(config_key=user_key):
            available.append(profile)
    return available
