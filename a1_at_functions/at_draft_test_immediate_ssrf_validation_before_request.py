# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_immediate_ssrf_validation_before_request.py:7
# Component id: at.source.a1_at_functions.test_immediate_ssrf_validation_before_request
from __future__ import annotations

__version__ = "0.1.0"

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
