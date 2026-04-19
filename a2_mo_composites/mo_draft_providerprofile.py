# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_providerprofile.py:7
# Component id: mo.source.a2_mo_composites.providerprofile
from __future__ import annotations

__version__ = "0.1.0"

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
