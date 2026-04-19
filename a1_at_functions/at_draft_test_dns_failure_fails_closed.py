# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateurl.py:27
# Component id: at.source.a1_at_functions.test_dns_failure_fails_closed
from __future__ import annotations

__version__ = "0.1.0"

def test_dns_failure_fails_closed(self, monkeypatch: pytest.MonkeyPatch) -> None:
    def _raise_dns(*_args, **_kwargs):
        raise OSError("dns failure")

    monkeypatch.setattr("ass_ade.nexus.validation._socket.getaddrinfo", _raise_dns)
    assert _is_private_host("example.com") is True
    with pytest.raises(ValueError, match="private/loopback"):
        validate_url("https://example.com")
