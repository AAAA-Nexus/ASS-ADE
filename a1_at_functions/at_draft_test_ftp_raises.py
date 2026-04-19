# Extracted from C:/!ass-ade/tests/test_validation.py:113
# Component id: at.source.ass_ade.test_ftp_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_ftp_raises(self) -> None:
    with pytest.raises(ValueError, match="http or https"):
        validate_url("ftp://example.com")
