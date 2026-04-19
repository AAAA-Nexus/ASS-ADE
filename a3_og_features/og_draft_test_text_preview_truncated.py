# Extracted from C:/!ass-ade/tests/test_workflows.py:168
# Component id: og.source.ass_ade.test_text_preview_truncated
from __future__ import annotations

__version__ = "0.1.0"

def test_text_preview_truncated(self) -> None:
    long_text = "A" * 200
    result = certify_output(_mock_client(), long_text)
    assert len(result.text_preview) == 120
