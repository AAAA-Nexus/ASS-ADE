# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_test_catalog_includes_groq_chutes_nexus.py:7
# Component id: qk.source.a0_qk_constants.test_catalog_includes_groq_chutes_nexus
from __future__ import annotations

__version__ = "0.1.0"

def test_catalog_includes_groq_chutes_nexus(self):
    """The three most important providers for a no-budget user must be in the catalog."""
    assert "groq" in FREE_PROVIDERS
    assert "chutes" in FREE_PROVIDERS
    assert "nexus" in FREE_PROVIDERS
