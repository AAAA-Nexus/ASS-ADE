# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testcertifyoutput.py:24
# Component id: og.source.a3_og_features.test_text_preview_truncated
from __future__ import annotations

__version__ = "0.1.0"

def test_text_preview_truncated(self) -> None:
    long_text = "A" * 200
    result = certify_output(_mock_client(), long_text)
    assert len(result.text_preview) == 120
