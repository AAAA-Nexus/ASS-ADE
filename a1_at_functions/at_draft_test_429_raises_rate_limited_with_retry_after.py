# Extracted from C:/!ass-ade/tests/test_errors.py:73
# Component id: at.source.ass_ade.test_429_raises_rate_limited_with_retry_after
from __future__ import annotations

__version__ = "0.1.0"

def test_429_raises_rate_limited_with_retry_after(self) -> None:
    with pytest.raises(NexusRateLimited) as exc_info:
        raise_for_status(429, retry_after=5.0)
    assert exc_info.value.retry_after == 5.0
