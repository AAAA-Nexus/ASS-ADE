# Extracted from C:/!ass-ade/tests/test_free_providers.py:693
# Component id: at.source.ass_ade.test_env_hydration_populates_os_environ
from __future__ import annotations

__version__ = "0.1.0"

def test_env_hydration_populates_os_environ(self, tmp_path, monkeypatch):
    from ass_ade.config import load_config
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    # Write a .env at project root
    (tmp_path / ".env").write_text("GROQ_API_KEY=from-env-file\n")
    (tmp_path / ".ass-ade").mkdir()
    config_path = tmp_path / ".ass-ade" / "config.json"
    load_config(config_path)
    assert os.getenv("GROQ_API_KEY") == "from-env-file"
