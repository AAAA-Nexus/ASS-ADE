# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateurl.py:19
# Component id: at.source.a1_at_functions.test_ftp_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_ftp_raises(self) -> None:
    with pytest.raises(ValueError, match="http or https"):
        validate_url("ftp://example.com")
