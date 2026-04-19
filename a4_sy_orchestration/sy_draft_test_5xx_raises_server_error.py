# Extracted from C:/!ass-ade/tests/test_errors.py:78
# Component id: sy.source.ass_ade.test_5xx_raises_server_error
from __future__ import annotations

__version__ = "0.1.0"

def test_5xx_raises_server_error(self) -> None:
    for code in (500, 502, 503, 504):
        with pytest.raises(NexusServerError) as exc_info:
            raise_for_status(code)
        assert exc_info.value.status_code == code
