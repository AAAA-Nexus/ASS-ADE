# Extracted from C:/!ass-ade/tests/test_free_providers.py:656
# Component id: mo.source.ass_ade.testconfigproviderfields
from __future__ import annotations

__version__ = "0.1.0"

class TestConfigProviderFields:
    def test_default_config_has_new_fields(self):
        from ass_ade.config import AssAdeConfig
        cfg = AssAdeConfig()
        assert cfg.lse_enabled is True
        assert cfg.tier_policy == {}
        assert cfg.provider_fallback_chain == []
        assert cfg.providers == {}

    def test_provider_override_parses_from_json(self):
        from ass_ade.config import AssAdeConfig
        cfg = AssAdeConfig.model_validate({
            "profile": "local",
            "providers": {
                "groq": {"enabled": True, "api_key": "sk-test"},
                "gemini": {"enabled": False},
            },
            "tier_policy": {"balanced": "groq"},
            "provider_fallback_chain": ["groq", "gemini", "ollama"],
        })
        assert cfg.providers["groq"].api_key == "sk-test"
        assert cfg.providers["gemini"].enabled is False
        assert cfg.tier_policy == {"balanced": "groq"}
        assert cfg.provider_fallback_chain == ["groq", "gemini", "ollama"]

    def test_write_config_does_not_persist_api_keys(self, tmp_path):
        from ass_ade.config import AssAdeConfig, ProviderOverride, write_default_config
        cfg = AssAdeConfig(
            profile="local",
            providers={"groq": ProviderOverride(enabled=True, api_key="sk-secret")},
        )
        path = tmp_path / "config.json"
        write_default_config(path, config=cfg, overwrite=True)
        written = path.read_text(encoding="utf-8")
        assert "sk-secret" not in written
        assert "nexus_api_key" not in written

    def test_env_hydration_populates_os_environ(self, tmp_path, monkeypatch):
        from ass_ade.config import load_config
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        # Write a .env at project root
        (tmp_path / ".env").write_text("GROQ_API_KEY=from-env-file\n")
        (tmp_path / ".ass-ade").mkdir()
        config_path = tmp_path / ".ass-ade" / "config.json"
        load_config(config_path)
        assert os.getenv("GROQ_API_KEY") == "from-env-file"

    def test_env_hydration_does_not_override_process_env(self, tmp_path, monkeypatch):
        from ass_ade.config import load_config
        monkeypatch.setenv("GROQ_API_KEY", "from-process")
        (tmp_path / ".env").write_text("GROQ_API_KEY=from-file\n")
        (tmp_path / ".ass-ade").mkdir()
        load_config(tmp_path / ".ass-ade" / "config.json")
        # Process env wins
        assert os.getenv("GROQ_API_KEY") == "from-process"
