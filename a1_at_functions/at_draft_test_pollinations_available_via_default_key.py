# Extracted from C:/!ass-ade/tests/test_free_providers.py:116
# Component id: at.source.ass_ade.test_pollinations_available_via_default_key
from __future__ import annotations

__version__ = "0.1.0"

def test_pollinations_available_via_default_key(self):
    p = get_provider("pollinations")
    assert p.is_available() is True
