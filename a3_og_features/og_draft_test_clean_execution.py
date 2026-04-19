# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testsafeexecute.py:8
# Component id: og.source.a3_og_features.test_clean_execution
from __future__ import annotations

__version__ = "0.1.0"

def test_clean_execution(self) -> None:
    result = safe_execute(_mock_client(), "search_web", "query text", agent_id="13608")
    assert result.shield_passed is True
    assert result.prompt_scan_passed is True
