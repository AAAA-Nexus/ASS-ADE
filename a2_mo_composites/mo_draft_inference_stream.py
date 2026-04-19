# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:421
# Component id: mo.source.ass_ade.inference_stream
from __future__ import annotations

__version__ = "0.1.0"

def inference_stream(self, prompt: str, **kwargs: Any) -> Iterator[str]:
    """/v1/inference/stream — streaming CoT inference. $0.100/call

    Yields text chunks as they arrive via SSE / chunked response.
    """
    with self._client.stream("POST", "/v1/inference/stream", json={"prompt": prompt, **kwargs}) as r:
        r.raise_for_status()
        for chunk in r.iter_text():
            if chunk:
                yield chunk
