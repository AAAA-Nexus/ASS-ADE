# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_local_provider_always_available.py:7
# Component id: at.source.a1_at_functions.test_local_provider_always_available
from __future__ import annotations

__version__ = "0.1.0"

def test_local_provider_always_available(self):
    p = get_provider("ollama")
    assert p.local is True
    assert p.is_available() is True  # always true for local
