# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_validation.py:101
# Component id: at.source.ass_ade.testvalidateurl
__version__ = "0.1.0"

class TestValidateUrl:
    def test_valid_https(self) -> None:
        assert validate_url("https://atomadic.tech") == "https://atomadic.tech"

    def test_valid_http(self) -> None:
        with pytest.raises(ValueError, match="private/loopback"):
            validate_url("http://localhost:8787")

    def test_no_scheme_raises(self) -> None:
        with pytest.raises(ValueError, match="http or https"):
            validate_url("atomadic.tech")

    def test_ftp_raises(self) -> None:
        with pytest.raises(ValueError, match="http or https"):
            validate_url("ftp://example.com")

    def test_no_host_raises(self) -> None:
        with pytest.raises(ValueError, match="valid host"):
            validate_url("https://")

    def test_dns_failure_fails_closed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def _raise_dns(*_args, **_kwargs):
            raise OSError("dns failure")

        monkeypatch.setattr("ass_ade.nexus.validation._socket.getaddrinfo", _raise_dns)
        assert _is_private_host("example.com") is True
        with pytest.raises(ValueError, match="private/loopback"):
            validate_url("https://example.com")
