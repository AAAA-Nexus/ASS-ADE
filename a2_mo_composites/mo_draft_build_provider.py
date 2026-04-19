# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/router.py:37
# Component id: mo.source.ass_ade.build_provider
__version__ = "0.1.0"

def build_provider(config: AssAdeConfig) -> ModelProvider:
    """Build the provider stack for this config.

    Returns a `MultiProvider` if more than one provider is available, or a
    single provider instance if only one fits. Callers shouldn't care — they
    just invoke `.complete(request)`.
    """
    # Lazy import to break the circular dependency
    # (engine/__init__ → router → agent.providers → agent/__init__ → agent.loop → tools.registry → engine.types)
    from ass_ade.agent.providers import (
        DEFAULT_FALLBACK_CHAIN,
        FREE_PROVIDERS,
        detect_available_providers,
    )

    # 1. Explicit env override — highest priority, bypass catalog
    provider_url = os.getenv("ASS_ADE_PROVIDER_URL")
    if provider_url:
        return OpenAICompatibleProvider(
            base_url=provider_url,
            api_key=os.getenv("ASS_ADE_PROVIDER_KEY", ""),
            model=os.getenv("ASS_ADE_MODEL", "default"),
        )

    # 2. OpenAI env key → always add it as a registered provider
    # (Users who set OPENAI_API_KEY explicitly get it in the chain, but it
    # isn't listed in FREE_PROVIDERS because it's not free.)
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    # 3. Build provider map from catalog
    config_providers = {
        name: override.model_dump() for name, override in config.providers.items()
    } if hasattr(config, "providers") else {}

    available_profiles = detect_available_providers(config_providers)

    providers: dict[str, ModelProvider] = {}
    model_to_provider: dict[str, str] = {}

    for profile in available_profiles:
        if profile.base_url is None:
            continue  # requires custom URL (e.g., cloudflare); skip until user provides
        user_override = config_providers.get(profile.name, {}) if config_providers else {}

        # ── Special providers (Nexus) use their own class ────────────────
        if profile.special and profile.name == "nexus":
            # Priority: per-provider override → env var → top-level nexus_api_key
            api_key = (
                profile.resolve_api_key(config_key=user_override.get("api_key"))
                or config.nexus_api_key
            )
            if api_key and config.profile != "local":
                from ass_ade.nexus.client import NexusClient

                nexus_base = user_override.get("base_url") or profile.base_url or config.nexus_base_url
                client = NexusClient(
                    base_url=nexus_base,
                    api_key=api_key,
                    agent_id=config.agent_id,  # claim accrued LoRA credit automatically
                )
                providers["nexus"] = NexusProvider(client)
                override_models = user_override.get("models_by_tier") or {}
                for model_id in {**profile.models_by_tier, **override_models}.values():
                    if model_id:
                        model_to_provider[model_id] = "nexus"
            continue

        base_url = user_override.get("base_url") or profile.base_url
        api_key = profile.resolve_api_key(config_key=user_override.get("api_key"))
        default_model = _default_model(profile, user_override)
        inst = OpenAICompatibleProvider(
            base_url=base_url,
            api_key=api_key or "",
            model=default_model,
            timeout=config.request_timeout_s if config.request_timeout_s >= 10 else 60.0,
        )
        providers[profile.name] = inst
        # Register every model id this provider can serve
        override_models = user_override.get("models_by_tier") or {}
        for tier, model_id in {**profile.models_by_tier, **override_models}.items():
            if model_id:
                model_to_provider[model_id] = profile.name

    # 4. Add OpenAI if key present (bypasses free catalog)
    if openai_key:
        providers["openai"] = OpenAICompatibleProvider(
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            api_key=openai_key,
            model=os.getenv("ASS_ADE_MODEL", "gpt-4o"),
        )
        model_to_provider.setdefault("gpt-4o", "openai")
        model_to_provider.setdefault("gpt-4o-mini", "openai")

    # 5. Add Anthropic if key present (native Messages API)
    if anthropic_key:
        providers["anthropic"] = AnthropicProvider(
            api_key=anthropic_key,
            model=os.getenv("ASS_ADE_MODEL", "claude-sonnet-4-6"),
        )
        for m in ("claude-sonnet-4-6", "claude-opus-4-7", "claude-haiku-4-5-20251001"):
            model_to_provider.setdefault(m, "anthropic")

    # 6. Nexus handled above via catalog — skip duplicate wiring

    # 7. If nothing is configured, fall back to Ollama on localhost (free, local)
    if not providers:
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        return OpenAICompatibleProvider(
            base_url=f"{ollama_host}/v1",
            api_key="ollama",
            model=os.getenv("ASS_ADE_MODEL", "qwen2.5-coder:7b"),
        )

    # 8. Build MultiProvider with configured fallback order
    fallback_order = _build_fallback_order(config, providers)
    # Single-provider shortcut (no routing overhead)
    if len(providers) == 1:
        return next(iter(providers.values()))
    return MultiProvider(
        providers=providers,
        model_to_provider=model_to_provider,
        fallback_order=fallback_order,
    )
