# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_401_raises_auth_error.py:7
# Component id: at.source.a1_at_functions.test_401_raises_auth_error
from __future__ import annotations

__version__ = "0.1.0"

def test_401_raises_auth_error(self) -> None:
    with pytest.raises(NexusAuthError) as exc_info:
        raise_for_status(401, endpoint="/v1/trust/score")
    assert exc_info.value.status_code == 401
