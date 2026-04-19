# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testproviderprofile.py:5
# Component id: mo.source.ass_ade.testproviderprofile
__version__ = "0.1.0"

class TestProviderProfile:
    def test_resolve_api_key_config_wins(self):
        p = get_provider("groq")
        assert p is not None
        resolved = p.resolve_api_key(config_key="my-config-key")
        assert resolved == "my-config-key"

    def test_resolve_api_key_falls_back_to_env(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "env-key-value")
        p = get_provider("groq")
        assert p.resolve_api_key() == "env-key-value"

    def test_resolve_api_key_returns_none_when_missing(self, monkeypatch):
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        p = get_provider("groq")
        assert p.resolve_api_key() is None

    def test_local_provider_always_available(self):
        p = get_provider("ollama")
        assert p.local is True
        assert p.is_available() is True  # always true for local

    def test_cloud_provider_unavailable_without_key(self, monkeypatch):
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        p = get_provider("groq")
        assert p.is_available() is False

    def test_cloud_provider_available_with_env_key(self, monkeypatch):
        monkeypatch.setenv("GROQ_API_KEY", "sk-test")
        p = get_provider("groq")
        assert p.is_available() is True

    def test_pollinations_available_via_default_key(self):
        p = get_provider("pollinations")
        assert p.is_available() is True

    def test_model_for_tier_honors_override(self):
        p = get_provider("groq")
        override = {"fast": "my-custom-model"}
        assert p.model_for_tier("fast", override=override) == "my-custom-model"
        # Other tiers unaffected
        assert p.model_for_tier("deep", override=override) == p.models_by_tier["deep"]

    def test_model_for_tier_accepts_claude_aliases(self):
        p = get_provider("groq")
        assert p.model_for_tier("haiku") == p.models_by_tier["fast"]
        assert p.model_for_tier("sonnet") == p.models_by_tier["balanced"]
        assert p.model_for_tier("opus") == p.models_by_tier["deep"]
