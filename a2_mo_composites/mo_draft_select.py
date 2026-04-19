# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_lseengine.py:33
# Component id: mo.source.ass_ade.select
__version__ = "0.1.0"

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
