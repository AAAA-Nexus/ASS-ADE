# Extracted from C:/!ass-ade/tests/test_validation.py:105
# Component id: at.source.ass_ade.test_valid_http
from __future__ import annotations

__version__ = "0.1.0"

def test_valid_http(self) -> None:
    with pytest.raises(ValueError, match="private/loopback"):
        validate_url("http://localhost:8787")
