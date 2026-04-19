# Extracted from C:/!ass-ade/tests/test_free_providers.py:101
# Component id: at.source.ass_ade.test_local_provider_always_available
from __future__ import annotations

__version__ = "0.1.0"

def test_local_provider_always_available(self):
    p = get_provider("ollama")
    assert p.local is True
    assert p.is_available() is True  # always true for local
