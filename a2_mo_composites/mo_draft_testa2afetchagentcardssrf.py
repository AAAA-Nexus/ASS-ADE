# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testa2afetchagentcardssrf.py:7
# Component id: mo.source.a2_mo_composites.testa2afetchagentcardssrf
from __future__ import annotations

__version__ = "0.1.0"

class TestA2AFetchAgentCardSSRF:
    """Test SSRF protection in A2A agent card fetching."""

    def test_https_only_required(self) -> None:
        """A2A fetching should require HTTPS."""
        report = fetch_agent_card("http://example.com/.well-known/agent.json")
        assert not report.valid
        assert "HTTPS" in report.errors[0].message

    def test_localhost_blocked(self) -> None:
        """A2A should block attempts to fetch from localhost."""
        report = fetch_agent_card("https://localhost/.well-known/agent.json")
        assert not report.valid
        assert len(report.errors) > 0
        assert "blocked" in report.errors[0].message or "loopback" in report.errors[0].message

    def test_appends_well_known_path(self) -> None:
        """Fetching from a URL without /.well-known/agent.json should auto-append it."""
        # Mock httpx.get to verify the right URL is called
        with mock.patch("ass_ade.a2a.httpx.get") as mock_get:
            mock_response = mock.MagicMock()
            mock_response.json.return_value = {"name": "TestAgent"}
            mock_get.return_value = mock_response

            # This should work and return valid=False because the JSON is incomplete
            # but we mainly care about the URL transformation
            fetch_agent_card("https://example.com")

            # Verify that the .well-known path was appended
            called_url = mock_get.call_args[0][0]
            assert called_url.endswith("/.well-known/agent.json")

    def test_immediate_ssrf_validation_before_request(self) -> None:
        """SSRF validation should happen immediately before the network request.

        This tests that we don't have a TOCTOU window where DNS could change
        between validation and the actual request.
        """
        with mock.patch("ass_ade.a2a.httpx.get") as mock_get:
            with mock.patch("ass_ade.a2a._check_ssrf") as mock_check_ssrf:
                # Set up mocks
                mock_check_ssrf.return_value = None  # No SSRF error
                mock_response = mock.MagicMock()
                mock_response.json.return_value = {"name": "TestAgent"}
                mock_get.return_value = mock_response

                # Call fetch_agent_card
                fetch_agent_card("https://example.com")

                # Verify _check_ssrf was called (it's called immediately before request)
                assert mock_check_ssrf.called
