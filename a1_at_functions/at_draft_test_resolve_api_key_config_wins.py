# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_resolve_api_key_config_wins.py:7
# Component id: at.source.a1_at_functions.test_resolve_api_key_config_wins
from __future__ import annotations

__version__ = "0.1.0"

def test_resolve_api_key_config_wins(self):
    p = get_provider("groq")
    assert p is not None
    resolved = p.resolve_api_key(config_key="my-config-key")
    assert resolved == "my-config-key"
