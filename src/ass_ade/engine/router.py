"""Model router — picks the best provider(s) for a given config.

Strategy (updated for free-provider catalog support):
  1. If explicit env overrides are set (ASS_ADE_PROVIDER_URL, OPENAI_API_KEY,
     ANTHROPIC_API_KEY), build a single-provider instance for backwards compat.
  2. Otherwise, auto-discover every provider in the free-provider catalog
     whose API key is present (env or config override) and bundle them into
     a `MultiProvider` that LSE can route to per-step.
  3. In hybrid/premium profiles with a Nexus API key, the NexusProvider is
     registered alongside the free ones (and can be selected by name).
  4. Final fallback: Pollinations (no key) + Ollama (local).

The returned `ModelProvider` is always LSE-aware: when LSE emits a model id,
the MultiProvider routes to the underlying provider that serves it.
"""

from __future__ import annotations

import os
from typing import Any

from typing import TYPE_CHECKING

from ass_ade.config import AssAdeConfig
from ass_ade.engine.provider import (
    AnthropicProvider,
    ModelProvider,
    MultiProvider,
    NexusProvider,
    OpenAICompatibleProvider,
)

if TYPE_CHECKING:
    from ass_ade.agent.providers import ProviderProfile


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


def _default_model(profile: "ProviderProfile", user_override: dict[str, Any]) -> str:
    """Pick a sensible default model for a provider.

    Priority: user-override fast → profile fast → any model we know about.
    """
    override_models = user_override.get("models_by_tier") or {}
    for tier in ("fast", "balanced", "deep"):
        if override_models.get(tier):
            return override_models[tier]
        if profile.models_by_tier.get(tier):
            return profile.models_by_tier[tier]
    return "default"


def _build_fallback_order(
    config: AssAdeConfig, providers: dict[str, ModelProvider]
) -> list[str]:
    """Compute the ordered list of providers to try in turn."""
    from ass_ade.agent.providers import DEFAULT_FALLBACK_CHAIN

    configured = list(getattr(config, "provider_fallback_chain", []) or [])
    known = list(providers.keys())
    order: list[str] = []
    # 1. Honor configured order (only for names we actually have)
    for name in configured:
        if name in providers and name not in order:
            order.append(name)
    # 2. Then the catalog default order (only for names we have)
    for name in DEFAULT_FALLBACK_CHAIN:
        if name in providers and name not in order:
            order.append(name)
    # 3. Finally any leftover providers (openai, anthropic, nexus)
    for name in known:
        if name not in order:
            order.append(name)
    return order
