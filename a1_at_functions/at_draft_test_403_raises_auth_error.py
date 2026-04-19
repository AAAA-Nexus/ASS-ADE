# Extracted from C:/!ass-ade/tests/test_errors.py:60
# Component id: at.source.ass_ade.test_403_raises_auth_error
from __future__ import annotations

__version__ = "0.1.0"

def test_403_raises_auth_error(self) -> None:
    with pytest.raises(NexusAuthError):
        raise_for_status(403)
