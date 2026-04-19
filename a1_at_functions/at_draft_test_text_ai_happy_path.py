# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_text_ai_happy_path.py:7
# Component id: at.source.a1_at_functions.test_text_ai_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_text_ai_happy_path(method_name, response_json):
    """Test text AI methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "text_summarize":
            result = client.text_summarize(text="long text content")
        elif method_name == "text_keywords":
            result = client.text_keywords(text="text with keywords", top_k=10)
        else:  # text_sentiment
            result = client.text_sentiment(text="positive content")
        assert result is not None
