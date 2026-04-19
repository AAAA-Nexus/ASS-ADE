# Extracted from C:/!ass-ade/tests/test_free_providers.py:85
# Component id: at.source.ass_ade.test_resolve_api_key_config_wins
from __future__ import annotations

__version__ = "0.1.0"

def test_resolve_api_key_config_wins(self):
    p = get_provider("groq")
    assert p is not None
    resolved = p.resolve_api_key(config_key="my-config-key")
    assert resolved == "my-config-key"
