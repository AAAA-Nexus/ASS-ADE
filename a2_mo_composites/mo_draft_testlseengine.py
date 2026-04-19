# Extracted from C:/!ass-ade/tests/test_phase_engines.py:17
# Component id: mo.source.ass_ade.testlseengine
from __future__ import annotations

__version__ = "0.1.0"

class TestLSEEngine:
    def _make(self, cfg=None):
        from ass_ade.agent.lse import LSEEngine
        return LSEEngine(cfg or {})

    def _no_providers_cfg(self, monkeypatch=None):
        """Build an LSE config that disables every catalog provider so the
        legacy Claude fallback kicks in deterministically."""
        from ass_ade.agent.providers import FREE_PROVIDERS
        if monkeypatch is not None:
            for p in FREE_PROVIDERS.values():
                if p.api_key_env:
                    monkeypatch.delenv(p.api_key_env, raising=False)
        return {"providers": {name: {"enabled": False} for name in FREE_PROVIDERS}}

    def test_default_returns_balanced_tier(self, monkeypatch):
        # With every catalog provider disabled (incl. pollinations), LSE falls
        # back to the legacy Claude sonnet id.
        lse = self._make(self._no_providers_cfg(monkeypatch))
        decision = lse.select(trs_score=0.75, complexity="medium")
        assert decision.tier == "balanced"
        assert decision.model == "claude-sonnet-4-6"

    def test_high_trs_simple_task_gives_fast(self):
        lse = self._make()
        decision = lse.select(trs_score=0.95, complexity="simple")
        assert decision.tier == "fast"

    def test_low_trs_complex_task_gives_deep(self):
        lse = self._make()
        decision = lse.select(trs_score=0.3, complexity="complex")
        assert decision.tier == "deep"

    def test_critical_complexity_always_deep(self):
        lse = self._make()
        decision = lse.select(trs_score=0.9, complexity="critical")
        assert decision.tier == "deep"

    def test_user_override_wins(self):
        lse = self._make()
        decision = lse.select(trs_score=0.1, complexity="trivial", user_model_override="my-custom-model")
        assert decision.model == "my-custom-model"
        assert decision.reason == "user_override"

    def test_budget_pressure_downgrades_to_fast(self):
        lse = self._make()
        decision = lse.select(trs_score=0.8, complexity="complex", budget_remaining=500)
        assert decision.tier == "fast"
        assert "budget_pressure" in decision.reason

    def test_fail_open_on_internal_error(self):
        lse = self._make({"lse": {"default_tier": "balanced"}})
        # Corrupt internal state — should still return a decision
        lse._trs_haiku_threshold = "not_a_float"  # type: ignore
        decision = lse.select(trs_score=0.9)
        assert decision.model is not None

    def test_report_tracks_decisions(self):
        lse = self._make()
        lse.select(trs_score=0.8)
        lse.select(trs_score=0.5)
        rep = lse.report()
        assert rep["decisions"] == 2
        assert "tier_distribution" in rep
        assert "provider_distribution" in rep
        assert "avg_trs" in rep

    def test_legacy_fallback_uses_claude_model_ids(self):
        """When no free providers are configured, LSE falls back to Claude models."""
        from ass_ade.agent.lse import _LEGACY_TIER_TO_MODEL
        assert "claude" in _LEGACY_TIER_TO_MODEL["fast"]
        assert "claude" in _LEGACY_TIER_TO_MODEL["balanced"]
        assert "claude" in _LEGACY_TIER_TO_MODEL["deep"]

    def test_claude_tier_alias_in_tier_policy(self):
        """tier_policy should accept 'haiku'/'sonnet'/'opus' aliases."""
        lse = self._make({"tier_policy": {"sonnet": "groq"}})
        # The policy key should have been normalized to 'balanced'
        assert lse._tier_policy == {"balanced": "groq"}
