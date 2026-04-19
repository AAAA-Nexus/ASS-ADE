# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_write_config_does_not_persist_api_keys.py:7
# Component id: at.source.a1_at_functions.test_write_config_does_not_persist_api_keys
from __future__ import annotations

__version__ = "0.1.0"

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
