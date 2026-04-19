# Extracted from C:/!ass-ade/tests/test_validation.py:109
# Component id: at.source.ass_ade.test_no_scheme_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_no_scheme_raises(self) -> None:
    with pytest.raises(ValueError, match="http or https"):
        validate_url("atomadic.tech")
