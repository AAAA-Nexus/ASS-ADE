# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testlsewithcatalog.py:21
# Component id: at.source.ass_ade.test_lse_falls_back_to_pollinations_when_catalog_disabled
__version__ = "0.1.0"

    def test_lse_falls_back_to_pollinations_when_catalog_disabled(self, monkeypatch):
        """Without any free provider keys AND pollinations explicitly disabled,
        LSE falls back to legacy Claude sonnet."""
        for p in FREE_PROVIDERS.values():
            if p.api_key_env:
                monkeypatch.delenv(p.api_key_env, raising=False)
        # Disable EVERY catalog entry (including pollinations, the no-key default)
        disabled_cfg = {name: {"enabled": False} for name in FREE_PROVIDERS}
        from ass_ade.agent.lse import LSEEngine, _LEGACY_TIER_TO_MODEL

        lse = LSEEngine({"providers": disabled_cfg})
        decision = lse.select(trs_score=0.8, complexity="medium")
        # With pollinations disabled, the only remaining fallback is the legacy Claude id
        assert decision.provider is None
        assert decision.model == _LEGACY_TIER_TO_MODEL["balanced"]
