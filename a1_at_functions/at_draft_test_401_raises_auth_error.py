# Extracted from C:/!ass-ade/tests/test_errors.py:55
# Component id: at.source.ass_ade.test_401_raises_auth_error
from __future__ import annotations

__version__ = "0.1.0"

def test_401_raises_auth_error(self) -> None:
    with pytest.raises(NexusAuthError) as exc_info:
        raise_for_status(401, endpoint="/v1/trust/score")
    assert exc_info.value.status_code == 401
