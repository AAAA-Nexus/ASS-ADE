# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/providers.py:385
# Component id: at.source.ass_ade.select_provider_for_tier
__version__ = "0.1.0"

def select_provider_for_tier(
    tier: str,
    *,
    fallback_chain: list[str] | None = None,
    config_providers: dict[str, Any] | None = None,
    tier_policy: dict[str, str] | None = None,
) -> tuple[ProviderProfile, str] | None:
    """Select (provider, model) for a given tier.

    Priority:
      1. `tier_policy[tier]` — explicit user override ("use gemini for balanced")
      2. First provider in `fallback_chain` that is available AND has a model for this tier
      3. None if nothing matches (caller must handle)
    """
    canonical = resolve_tier(tier)
    overrides = config_providers or {}

    # 1. Explicit tier → provider policy
    if tier_policy and canonical in tier_policy:
        pref_name = tier_policy[canonical]
        profile = get_provider(pref_name)
        if profile is not None:
            user_override = overrides.get(pref_name) if overrides else None
            user_key = None
            override_models = None
            if isinstance(user_override, dict):
                user_key = user_override.get("api_key")
                override_models = user_override.get("models_by_tier")
            if profile.is_available(config_key=user_key):
                model = profile.model_for_tier(canonical, override=override_models)
                if model:
                    return profile, model

    # 2. Fallback chain
    chain = fallback_chain or DEFAULT_FALLBACK_CHAIN
    for name in chain:
        profile = get_provider(name)
        if profile is None:
            continue
        user_override = overrides.get(name) if overrides else None
        user_key = None
        override_models = None
        enabled = True
        if isinstance(user_override, dict):
            user_key = user_override.get("api_key")
            override_models = user_override.get("models_by_tier")
            enabled = user_override.get("enabled", True)
        if not enabled:
            continue
        if not profile.is_available(config_key=user_key):
            continue
        model = profile.model_for_tier(canonical, override=override_models)
        if model:
            return profile, model

    return None
