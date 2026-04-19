# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/config.py:27
# Component id: mo.source.ass_ade.assadeconfig
__version__ = "0.1.0"

class AssAdeConfig(BaseModel):
    profile: ProfileName = Field(default="local")
    nexus_base_url: str = Field(default="https://atomadic.tech")
    request_timeout_s: float = Field(default=20.0, ge=1.0, le=120.0)
    agent_id: str = Field(default="ass-ade-local")
    agent_model: str = Field(default="")  # empty = let LSE + catalog decide
    nexus_api_key: str | None = Field(default=None, repr=False)

    # ── LSE + Provider configuration (Phase 1 free-tier support) ─────────
    lse_enabled: bool = Field(default=True)
    """Enable LSE tier-based model routing. If False, agent_model is used directly."""

    tier_policy: dict[str, str] = Field(default_factory=dict)
    """Explicit tier → provider preference, e.g. {"balanced": "groq", "deep": "openrouter"}.
    Keys: fast / balanced / deep. Values: provider names from the catalog."""

    provider_fallback_chain: list[str] = Field(default_factory=list)
    """Ordered list of provider names to try. Empty = use catalog default."""

    providers: dict[str, ProviderOverride] = Field(default_factory=dict)
    """Per-provider overrides. Key = provider name (groq, gemini, ollama, ...)."""
