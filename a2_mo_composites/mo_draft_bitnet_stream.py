# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1079
# Component id: mo.source.a2_mo_composites.bitnet_stream
from __future__ import annotations

__version__ = "0.1.0"

def bitnet_stream(self, prompt: str, model: str = "bitnet-b1.58-2B-4T", **kwargs: Any) -> Iterator[str]:
    """POST /v1/bitnet/inference/stream — streaming 1-bit CoT (BIT-101). $0.040/call"""
    with self._client.stream("POST", "/v1/bitnet/inference/stream", json={"prompt": prompt, "model": model, **kwargs}) as r:
        r.raise_for_status()
        for chunk in r.iter_text():
            if chunk:
                yield chunk
