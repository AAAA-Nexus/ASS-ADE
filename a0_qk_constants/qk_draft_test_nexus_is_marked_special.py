# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testcataloginvariants.py:14
# Component id: qk.source.a0_qk_constants.test_nexus_is_marked_special
from __future__ import annotations

__version__ = "0.1.0"

def test_nexus_is_marked_special(self):
    """Nexus uses NexusProvider, not OpenAICompatibleProvider."""
    assert FREE_PROVIDERS["nexus"].special is True
