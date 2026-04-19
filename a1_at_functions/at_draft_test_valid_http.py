# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateurl.py:11
# Component id: at.source.a1_at_functions.test_valid_http
from __future__ import annotations

__version__ = "0.1.0"

def test_valid_http(self) -> None:
    with pytest.raises(ValueError, match="private/loopback"):
        validate_url("http://localhost:8787")
