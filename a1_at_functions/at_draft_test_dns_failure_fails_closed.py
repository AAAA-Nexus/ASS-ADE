# Extracted from C:/!ass-ade/tests/test_validation.py:121
# Component id: at.source.ass_ade.test_dns_failure_fails_closed
from __future__ import annotations

__version__ = "0.1.0"

def test_dns_failure_fails_closed(self, monkeypatch: pytest.MonkeyPatch) -> None:
    def _raise_dns(*_args, **_kwargs):
        raise OSError("dns failure")

    monkeypatch.setattr("ass_ade.nexus.validation._socket.getaddrinfo", _raise_dns)
    assert _is_private_host("example.com") is True
    with pytest.raises(ValueError, match="private/loopback"):
        validate_url("https://example.com")
