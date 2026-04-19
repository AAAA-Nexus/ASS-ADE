# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testcertifyoutput.py:20
# Component id: og.source.a3_og_features.test_empty_text_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_text_raises(self) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        certify_output(_mock_client(), "")
