# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_complete_basic.py:7
# Component id: at.source.a1_at_functions.test_complete_basic
from __future__ import annotations

__version__ = "0.1.0"

def test_complete_basic(self, mock_client_cls):
    mock_resp = MagicMock()
    mock_resp.json.return_value = self._mock_response("Hello!")
    mock_resp.raise_for_status = MagicMock()

    mock_instance = MagicMock()
    mock_instance.post.return_value = mock_resp
    mock_client_cls.return_value = mock_instance

    provider = OpenAICompatibleProvider(base_url="http://test:8000/v1", api_key="k")
    req = CompletionRequest(messages=[Message(role="user", content="hi")])
    resp = provider.complete(req)

    assert resp.message.content == "Hello!"
    assert resp.finish_reason == "stop"
    assert resp.model == "test-model"
