# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_lseengine.py:5
# Component id: mo.source.ass_ade.lseengine
__version__ = "0.1.0"

class LSEEngine:
    """LLM Selection Engine — routes each agent step to the optimal model.

    Consults the free-provider catalog so users without paid API keys get
    free models selected automatically. Users can:
      - Force a specific provider per tier via `config["tier_policy"]`
      - Reorder the fallback chain via `config["provider_fallback_chain"]`
      - Override per-provider models via `config["providers"][name].models_by_tier`
    """

    def __init__(self, config: dict[str, Any] | None = None, nexus: Any = None) -> None:
        self._config = config or {}
        self._nexus = nexus
        cfg = self._config.get("lse") or {}
        self._default_tier = resolve_tier(cfg.get("default_tier", TIER_BALANCED))
        self._trs_haiku_threshold = float(cfg.get("trs_haiku_threshold", 0.85))
        self._trs_opus_threshold = float(cfg.get("trs_opus_threshold", 0.45))
        self._budget_floor_tokens = int(cfg.get("budget_floor_tokens", 2000))
        # Catalog-routing knobs
        self._tier_policy: dict[str, str] = dict(self._config.get("tier_policy") or {})
        self._fallback_chain: list[str] = list(self._config.get("provider_fallback_chain") or [])
        self._providers_cfg: dict[str, Any] = dict(self._config.get("providers") or {})
        # Aliased policy keys (haiku→fast etc.)
        self._tier_policy = {
            resolve_tier(k): v for k, v in self._tier_policy.items()
        }
        self._decisions: list[LSEDecision] = []

    def select(
        self,
        *,
        trs_score: float = 0.8,
        complexity: str = "medium",
        budget_remaining: int = 8000,
        user_model_override: str | None = None,
    ) -> LSEDecision:
        """Select the optimal model for a step.

        Args:
            trs_score: SAM TRS composite score [0,1].
            complexity: EpistemicRouter complexity bucket.
            budget_remaining: Estimated remaining output tokens.
            user_model_override: Explicit model from CLI/config (always wins).
        """
        try:
            return self._select_inner(trs_score, complexity, budget_remaining, user_model_override)
        except Exception as exc:
            _log.warning("LSE selection failed (fail-open): %s", exc)
            legacy = _LEGACY_TIER_TO_MODEL.get(self._default_tier, _LEGACY_TIER_TO_MODEL[TIER_BALANCED])
            return LSEDecision(
                model=legacy,
                tier=self._default_tier,
                reason="fallback",
                trs_score=trs_score,
                complexity=complexity,
                provider=None,
            )

    def _select_inner(
        self,
        trs_score: float,
        complexity: str,
        budget_remaining: int,
        user_model_override: str | None,
    ) -> LSEDecision:
        if user_model_override:
            return LSEDecision(
                model=user_model_override,
                tier=TIER_BALANCED,
                reason="user_override",
                trs_score=trs_score,
                complexity=complexity,
                provider=None,
            )

        # 1. Start from complexity floor
        complexity_key = (complexity or "medium").lower()
        floor_tier = _COMPLEXITY_FLOOR.get(complexity_key, TIER_BALANCED)
        tier = floor_tier

        # 2. TRS modulation: high confidence on simple task → FAST
        if trs_score >= self._trs_haiku_threshold and _TIER_INDEX.get(tier, 1) <= _TIER_INDEX[TIER_BALANCED]:
            tier = _max_tier(floor_tier, TIER_FAST)
            reason = f"trs_high({trs_score:.2f})_downgrade"
        elif trs_score <= self._trs_opus_threshold:
            tier = _max_tier(tier, TIER_DEEP)
            reason = f"trs_low({trs_score:.2f})_upgrade"
        else:
            reason = f"complexity({complexity_key})"

        # 3. Budget pressure: very few tokens → FAST
        if budget_remaining < self._budget_floor_tokens and _TIER_INDEX.get(tier, 1) > _TIER_INDEX[TIER_FAST]:
            tier = TIER_FAST
            reason = f"budget_pressure({budget_remaining}tok)"

        # 4. Resolve tier → (provider, model) via catalog
        provider_name, model = self._resolve_tier_to_model(tier)

        decision = LSEDecision(
            model=model,
            tier=tier,
            reason=reason,
            trs_score=trs_score,
            complexity=complexity,
            provider=provider_name,
        )
        self._decisions.append(decision)
        return decision

    def _resolve_tier_to_model(self, tier: str) -> tuple[str | None, str]:
        """Consult the provider catalog. Falls back to pollinations (no-key)
        or legacy Claude ids as the last resort."""
        match = select_provider_for_tier(
            tier,
            fallback_chain=self._fallback_chain or None,
            config_providers=self._providers_cfg,
            tier_policy=self._tier_policy,
        )
        if match is not None:
            profile, model = match
            return profile.name, model

        # Nothing in the catalog matched — prefer pollinations (no-key) so
        # the caller gets a working endpoint instead of a Claude id that will
        # 401 without an Anthropic key. Respect explicit user disable.
        try:
            pol_cfg = self._providers_cfg.get("pollinations") or {}
            pol_enabled = pol_cfg.get("enabled", True)
            if pol_enabled:
                from ass_ade.agent.providers import get_provider
                pol = get_provider("pollinations")
                if pol is not None:
                    canonical = resolve_tier(tier)
                    model = pol.model_for_tier(canonical)
                    if model:
                        return "pollinations", model
        except Exception:
            pass

        # Truly last-ditch: legacy Claude model ids (require ANTHROPIC_API_KEY)
        return None, _LEGACY_TIER_TO_MODEL.get(tier, _LEGACY_TIER_TO_MODEL[TIER_BALANCED])

    def report(self) -> dict[str, Any]:
        if not self._decisions:
            return {"engine": "lse", "decisions": 0}
        tier_counts: dict[str, int] = {}
        provider_counts: dict[str, int] = {}
        for d in self._decisions:
            tier_counts[d.tier] = tier_counts.get(d.tier, 0) + 1
            if d.provider:
                provider_counts[d.provider] = provider_counts.get(d.provider, 0) + 1
        avg_trs = sum(d.trs_score for d in self._decisions) / len(self._decisions)
        last = self._decisions[-1]
        return {
            "engine": "lse",
            "decisions": len(self._decisions),
            "tier_distribution": tier_counts,
            "provider_distribution": provider_counts,
            "avg_trs": round(avg_trs, 3),
            "last_model": last.model,
            "last_provider": last.provider,
            "last_tier": last.tier,
        }
