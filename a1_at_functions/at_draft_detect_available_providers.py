# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/providers.py:355
# Component id: at.source.ass_ade.detect_available_providers
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
