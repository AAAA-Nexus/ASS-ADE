# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testraiseforstatus.py:35
# Component id: sy.source.a2_mo_composites.test_5xx_raises_server_error
from __future__ import annotations

__version__ = "0.1.0"

def test_5xx_raises_server_error(self) -> None:
    for code in (500, 502, 503, 504):
        with pytest.raises(NexusServerError) as exc_info:
            raise_for_status(code)
        assert exc_info.value.status_code == code
