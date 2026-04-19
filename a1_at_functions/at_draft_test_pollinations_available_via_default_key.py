# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_pollinations_available_via_default_key.py:7
# Component id: at.source.a1_at_functions.test_pollinations_available_via_default_key
from __future__ import annotations

__version__ = "0.1.0"

def test_pollinations_available_via_default_key(self):
    p = get_provider("pollinations")
    assert p.is_available() is True
