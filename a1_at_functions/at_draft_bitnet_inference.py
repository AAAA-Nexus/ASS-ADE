# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_bitnet_inference.py:7
# Component id: at.source.a1_at_functions.bitnet_inference
from __future__ import annotations

__version__ = "0.1.0"

def bitnet_inference(self, prompt: str, model: str = "bitnet-b1.58-2B-4T", **kwargs: Any) -> BitNetInferenceResponse:
    """POST /v1/bitnet/inference — 1-bit chat completion (BIT-100). $0.020/call"""
    return self._post_model("/v1/bitnet/inference", BitNetInferenceResponse, {"prompt": prompt, "model": model, **kwargs})
