# Extracted from C:/!ass-ade/tests/test_free_providers.py:630
# Component id: mo.source.ass_ade.testchutesprovider
from __future__ import annotations

__version__ = "0.1.0"

class TestChutesProvider:
    """Chutes.ai — free DeepSeek V3/R1 via Bittensor subnet."""

    def test_chutes_in_catalog(self):
        assert "chutes" in FREE_PROVIDERS

    def test_chutes_available_with_env_key(self, monkeypatch):
        monkeypatch.setenv("CHUTES_API_TOKEN", "ct_test_key")
        profile = get_provider("chutes")
        assert profile.is_available() is True

    def test_chutes_serves_deepseek_models(self):
        profile = get_provider("chutes")
        assert "deepseek" in profile.models_by_tier["balanced"].lower()
        assert "deepseek" in profile.models_by_tier["deep"].lower()

    def test_chutes_selectable_via_tier_policy(self, monkeypatch):
        monkeypatch.setenv("CHUTES_API_TOKEN", "ct_test_key")
        from ass_ade.agent.lse import LSEEngine

        lse = LSEEngine({"tier_policy": {"deep": "chutes"}})
        decision = lse.select(trs_score=0.3, complexity="critical")
        assert decision.provider == "chutes"
        assert "deepseek" in decision.model.lower()
