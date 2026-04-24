"""Tests for input validation layer."""

import pytest

from ass_ade.nexus.validation import (
    _is_private_host,
    validate_agent_id,
    validate_prompt,
    validate_session_id,
    validate_url,
    validate_usdc_amount,
)


class TestValidateAgentId:
    def test_valid_ids(self) -> None:
        assert validate_agent_id("agent-1") == "agent-1"
        assert validate_agent_id("13608") == "13608"
        assert validate_agent_id("my_agent.v2:latest") == "my_agent.v2:latest"

    def test_strips_whitespace(self) -> None:
        assert validate_agent_id("  agent-1  ") == "agent-1"

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            validate_agent_id("")

    def test_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            validate_agent_id("   ")

    def test_too_long_raises(self) -> None:
        with pytest.raises(ValueError, match="exceeds 256"):
            validate_agent_id("a" * 257)

    def test_invalid_chars_raises(self) -> None:
        with pytest.raises(ValueError, match="invalid characters"):
            validate_agent_id("agent id with spaces")
        with pytest.raises(ValueError, match="invalid characters"):
            validate_agent_id("agent<script>")


class TestValidatePrompt:
    def test_valid_prompt(self) -> None:
        assert validate_prompt("Hello world") == "Hello world"

    def test_strips_control_chars(self) -> None:
        result = validate_prompt("Hello\x00World\x0b!")
        assert "\x00" not in result
        assert "\x0b" not in result
        assert "HelloWorld!" == result

    def test_preserves_newlines_and_tabs(self) -> None:
        text = "Hello\nWorld\tFoo"
        assert validate_prompt(text) == text

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            validate_prompt("")

    def test_whitespace_only_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            validate_prompt("   ")

    def test_oversized_raises(self) -> None:
        with pytest.raises(ValueError, match="exceeds"):
            validate_prompt("x" * 40_000)


class TestValidateUsdcAmount:
    def test_valid_amounts(self) -> None:
        assert validate_usdc_amount(0.01) == 0.01
        assert validate_usdc_amount(1_000_000.0) == 1_000_000.0

    def test_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            validate_usdc_amount(0.0)

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            validate_usdc_amount(-5.0)

    def test_too_large_raises(self) -> None:
        with pytest.raises(ValueError, match="maximum"):
            validate_usdc_amount(1_000_001.0)


class TestValidateSessionId:
    def test_valid(self) -> None:
        assert validate_session_id("sess-abc-123") == "sess-abc-123"

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            validate_session_id("")

    def test_too_long_raises(self) -> None:
        with pytest.raises(ValueError, match="exceeds 256"):
            validate_session_id("x" * 257)


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
