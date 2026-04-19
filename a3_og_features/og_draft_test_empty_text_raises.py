# Extracted from C:/!ass-ade/tests/test_workflows.py:164
# Component id: og.source.ass_ade.test_empty_text_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_text_raises(self) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        certify_output(_mock_client(), "")
