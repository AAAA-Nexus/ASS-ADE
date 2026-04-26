"""Free Provider Catalog — the exhaustive list of free LLM providers.

Each `ProviderProfile` describes:
  - how to reach the provider (base_url, auth env var)
  - recommended models per tier (fast / balanced / deep)
  - whether it's local (no internet needed) or cloud

The LSE maps a selected tier → (provider, model) by looking up the
first available provider in the configured fallback chain that has an
API key present (env or config override).

All providers listed here have a permanent free tier as of 2026-04.
When a free tier is rate-limited, the `rate_limit` field documents it.

Add new providers here — do NOT hardcode model strings elsewhere.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

# Canonical tier names — provider-agnostic.
# Aliases are maintained for backwards compatibility with Claude tier names.
TIER_FAST = "fast"
TIER_BALANCED = "balanced"
TIER_DEEP = "deep"

TIER_ALIASES: dict[str, str] = {
    "haiku": TIER_FAST,
    "sonnet": TIER_BALANCED,
    "opus": TIER_DEEP,
    # plus the canonical names mapping to themselves
    TIER_FAST: TIER_FAST,
    TIER_BALANCED: TIER_BALANCED,
    TIER_DEEP: TIER_DEEP,
}

ALL_TIERS = (TIER_FAST, TIER_BALANCED, TIER_DEEP)


@dataclass
class ProviderProfile:
    """Describes a single LLM provider."""

    name: str
    display_name: str
    base_url: str | None  # None = requires runtime substitution (e.g., cloudflare account id)
    api_key_env: str | None  # environment variable name (None for local providers)
    api_key_default: str | None = None  # default key if none set (for local providers)
    local: bool = False  # True = runs on localhost, no internet needed
    models_by_tier: dict[str, str] = field(default_factory=dict)  # tier → model id
    signup_url: str | None = None
    rate_limit: str | None = None  # human-readable rate limit summary
    notes: str = ""
    # special=True → requires a custom provider class (NexusProvider), not
    # OpenAICompatibleProvider. The router knows how to instantiate it.
    special: bool = False
    # paid=True → not a free provider, but listed here so users can wire it in.
    paid: bool = False

    def resolve_api_key(self, config_key: str | None = None) -> str | None:
        """Resolve the API key: config override → env var → default."""
        if config_key:
            return config_key
        if self.api_key_env:
            env_val = os.getenv(self.api_key_env)
            if env_val:
                return env_val
        return self.api_key_default

    def model_for_tier(self, tier: str, override: dict[str, str] | None = None) -> str | None:
        """Get the model id for a tier, honoring config overrides."""
        tier = TIER_ALIASES.get(tier, tier)
        if override and tier in override:
            return override[tier]
        return self.models_by_tier.get(tier)

    def is_available(self, config_key: str | None = None) -> bool:
        """True if this provider has auth (or is local + reachable)."""
        if self.local:
            return True
        return self.resolve_api_key(config_key) is not None


# ─────────────────────────────────────────────────────────────────────────────
# The free provider catalog
# ─────────────────────────────────────────────────────────────────────────────

FREE_PROVIDERS: dict[str, ProviderProfile] = {
    # ─── Atomadic AAAA-Nexus (user's own key) ────────────────────────────
    "nexus": ProviderProfile(
        name="nexus",
        display_name="AAAA-Nexus (atomadic.tech)",
        base_url="https://atomadic.tech",  # actual routing goes through NexusClient
        api_key_env="AAAA_NEXUS_API_KEY",
        special=True,  # uses NexusProvider (NexusClient), not OpenAICompatibleProvider
        models_by_tier={
            TIER_FAST: "gemma-4-26b-a4b-it",
            TIER_BALANCED: "gemma-4-26b-a4b-it",
            TIER_DEEP: "gemma-4-26b-a4b-it",
        },
        signup_url="https://atomadic.tech/pay",
        rate_limit="Per-call metered ($0.060–0.100 via x402); quality-gated",
        notes="Your own AAAA-Nexus inference — hallucination oracle, trust gates, and attestations applied server-side.",
    ),
    # ─── Cloud free-tier providers ────────────────────────────────────────
    "groq": ProviderProfile(
        name="groq",
        display_name="Groq",
        base_url="https://api.groq.com/openai/v1",
        api_key_env="GROQ_API_KEY",
        models_by_tier={
            TIER_FAST: "llama-3.1-8b-instant",
            TIER_BALANCED: "llama-3.3-70b-versatile",
            TIER_DEEP: "llama-3.3-70b-versatile",
        },
        signup_url="https://console.groq.com",
        rate_limit="30 req/min free tier; very fast inference",
        notes="Extremely fast LPU-backed inference. Good default for most tasks.",
    ),
    "openrouter": ProviderProfile(
        name="openrouter",
        display_name="OpenRouter (free models)",
        base_url="https://openrouter.ai/api/v1",
        api_key_env="OPENROUTER_API_KEY",
        models_by_tier={
            TIER_FAST: "meta-llama/llama-3.2-3b-instruct:free",
            TIER_BALANCED: "meta-llama/llama-3.3-70b-instruct:free",
            TIER_DEEP: "deepseek/deepseek-r1:free",
        },
        signup_url="https://openrouter.ai/keys",
        rate_limit="20 req/min, 200 req/day on free models",
        notes="Aggregates many :free models. DeepSeek R1 has strong reasoning.",
    ),
    "gemini": ProviderProfile(
        name="gemini",
        display_name="Google Gemini",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai",
        api_key_env="GEMINI_API_KEY",
        models_by_tier={
            TIER_FAST: "gemini-2.0-flash-lite",
            TIER_BALANCED: "gemini-2.0-flash",
            TIER_DEEP: "gemini-2.5-pro",
        },
        signup_url="https://aistudio.google.com/apikey",
        rate_limit="15 req/min, 1500 req/day free",
        notes="Generous free tier. Gemini 2.5 Pro has long context (1M+ tokens).",
    ),
    "cerebras": ProviderProfile(
        name="cerebras",
        display_name="Cerebras",
        base_url="https://api.cerebras.ai/v1",
        api_key_env="CEREBRAS_API_KEY",
        models_by_tier={
            TIER_FAST: "llama3.1-8b",
            TIER_BALANCED: "llama3.3-70b",
            TIER_DEEP: "llama3.3-70b",
        },
        signup_url="https://cloud.cerebras.ai",
        rate_limit="30 req/min; ultra-fast wafer-scale inference",
        notes="Fastest free Llama inference available.",
    ),
    "mistral": ProviderProfile(
        name="mistral",
        display_name="Mistral La Plateforme",
        base_url="https://api.mistral.ai/v1",
        api_key_env="MISTRAL_API_KEY",
        models_by_tier={
            TIER_FAST: "mistral-small-latest",
            TIER_BALANCED: "mistral-medium-latest",
            TIER_DEEP: "mistral-large-latest",
        },
        signup_url="https://console.mistral.ai",
        rate_limit="Free experimentation tier",
        notes="European provider. Good at code and multilingual.",
    ),
    "github_models": ProviderProfile(
        name="github_models",
        display_name="GitHub Models",
        base_url="https://models.inference.ai.azure.com",
        api_key_env="GITHUB_TOKEN",
        models_by_tier={
            TIER_FAST: "gpt-4o-mini",
            TIER_BALANCED: "gpt-4o",
            TIER_DEEP: "o1",
        },
        signup_url="https://github.com/marketplace/models",
        rate_limit="Rate-limited free tier via GitHub",
        notes="Free access to GPT-4o and o1 via your GitHub account.",
    ),
    "huggingface": ProviderProfile(
        name="huggingface",
        display_name="Hugging Face Inference",
        base_url="https://api-inference.huggingface.co/v1",
        api_key_env="HF_TOKEN",
        models_by_tier={
            TIER_FAST: "meta-llama/Llama-3.2-3B-Instruct",
            TIER_BALANCED: "meta-llama/Llama-3.3-70B-Instruct",
            TIER_DEEP: "Qwen/Qwen2.5-Coder-32B-Instruct",
        },
        signup_url="https://huggingface.co/settings/tokens",
        rate_limit="Free tier shared across all HF models",
        notes="Huge model selection. Cold-start latency on less popular models.",
    ),
    "together": ProviderProfile(
        name="together",
        display_name="Together AI",
        base_url="https://api.together.xyz/v1",
        api_key_env="TOGETHER_API_KEY",
        models_by_tier={
            TIER_FAST: "meta-llama/Llama-3.2-3B-Instruct-Turbo",
            TIER_BALANCED: "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            TIER_DEEP: "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        },
        signup_url="https://api.together.xyz/settings/api-keys",
        rate_limit="$1 free credit + some :free suffix models",
        notes="High-quality infra. DeepSeek R1 distill is strong for coding.",
    ),
    "deepinfra": ProviderProfile(
        name="deepinfra",
        display_name="DeepInfra",
        base_url="https://api.deepinfra.com/v1/openai",
        api_key_env="DEEPINFRA_TOKEN",
        models_by_tier={
            TIER_FAST: "meta-llama/Llama-3.2-3B-Instruct",
            TIER_BALANCED: "meta-llama/Llama-3.3-70B-Instruct",
            TIER_DEEP: "Qwen/Qwen2.5-Coder-32B-Instruct",
        },
        signup_url="https://deepinfra.com/dash/api_keys",
        rate_limit="Free starter credits",
        notes="Pay-per-token with free starter credit.",
    ),
    "chutes": ProviderProfile(
        name="chutes",
        display_name="Chutes.ai (decentralized)",
        base_url="https://llm.chutes.ai/v1",
        api_key_env="CHUTES_API_TOKEN",
        models_by_tier={
            TIER_FAST: "unsloth/Llama-3.2-3B-Instruct",
            TIER_BALANCED: "deepseek-ai/DeepSeek-V3-0324",
            TIER_DEEP: "deepseek-ai/DeepSeek-R1",
        },
        signup_url="https://chutes.ai",
        rate_limit="Free tier with generous limits; decentralized Bittensor subnet 64",
        notes="Free DeepSeek V3 + R1 access. Decentralized inference on Bittensor.",
    ),
    "pollinations": ProviderProfile(
        name="pollinations",
        display_name="Pollinations AI",
        base_url="https://text.pollinations.ai/openai",
        api_key_env=None,
        api_key_default="anonymous",  # public endpoint, no key required
        models_by_tier={
            TIER_FAST: "openai",
            TIER_BALANCED: "openai-large",
            TIER_DEEP: "openai-reasoning",
        },
        signup_url=None,
        rate_limit="Anonymous; best-effort",
        notes="No signup required. Good fallback when no API keys set.",
    ),

    # ─── Local providers (completely free, no internet, no key needed) ───
    "ollama": ProviderProfile(
        name="ollama",
        display_name="Ollama (local)",
        base_url="http://localhost:11434/v1",
        api_key_env=None,
        api_key_default="ollama",
        local=True,
        models_by_tier={
            TIER_FAST: "qwen2.5-coder:1.5b",
            TIER_BALANCED: "qwen2.5-coder:7b",
            TIER_DEEP: "qwen2.5-coder:32b",
        },
        signup_url="https://ollama.com/download",
        rate_limit=None,
        notes="Run models locally. Pull models with 'ollama pull qwen2.5-coder:7b'.",
    ),
    "lmstudio": ProviderProfile(
        name="lmstudio",
        display_name="LM Studio (local)",
        base_url="http://localhost:1234/v1",
        api_key_env=None,
        api_key_default="lm-studio",
        local=True,
        models_by_tier={
            TIER_FAST: "local-model",
            TIER_BALANCED: "local-model",
            TIER_DEEP: "local-model",
        },
        signup_url="https://lmstudio.ai",
        rate_limit=None,
        notes="GUI for local models. Model names depend on what's loaded.",
    ),
    "llamacpp": ProviderProfile(
        name="llamacpp",
        display_name="llama.cpp server (local)",
        base_url="http://localhost:8080/v1",
        api_key_env=None,
        api_key_default="llama-cpp",
        local=True,
        models_by_tier={
            TIER_FAST: "local-model",
            TIER_BALANCED: "local-model",
            TIER_DEEP: "local-model",
        },
        signup_url="https://github.com/ggerganov/llama.cpp",
        rate_limit=None,
        notes="Start with './server -m model.gguf --host 0.0.0.0 --port 8080'.",
    ),
}


# Default fallback chain when user hasn't specified one.
# Order: fastest cloud-free → quality cloud-free → premium (Nexus) → local fallback
# Nexus is ranked high for users who have a key because it applies trust/hallucination
# gates server-side, but it is metered so it's placed after the free tier providers.
DEFAULT_FALLBACK_CHAIN: list[str] = [
    "groq",          # fastest cloud, free tier
    "cerebras",      # second-fastest, free tier
    "chutes",        # free DeepSeek V3/R1 via Bittensor
    "gemini",        # generous free quota
    "openrouter",    # many free models
    "mistral",       # free experimentation tier
    "together",      # :free-suffix models
    "github_models", # free GPT-4o/o1 via GitHub
    "huggingface",   # free HF inference
    "deepinfra",     # free starter credit
    "nexus",         # user's own AAAA-Nexus (metered, quality-gated)
    "pollinations",  # anonymous, no key
    "ollama",        # local, no internet needed
    "lmstudio",      # local GUI
    "llamacpp",      # local C++ server
]


# ─────────────────────────────────────────────────────────────────────────────
# Detection & resolution helpers
# ─────────────────────────────────────────────────────────────────────────────


def list_providers() -> list[str]:
    """All provider names known to the catalog."""
    return list(FREE_PROVIDERS.keys())


def get_provider(name: str) -> ProviderProfile | None:
    """Fetch a provider profile by name (case-insensitive)."""
    return FREE_PROVIDERS.get(name.lower())


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


def resolve_tier(tier: str) -> str:
    """Normalize a tier name (e.g., 'haiku' → 'fast'). Returns canonical tier."""
    return TIER_ALIASES.get(tier.lower(), tier.lower())


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
