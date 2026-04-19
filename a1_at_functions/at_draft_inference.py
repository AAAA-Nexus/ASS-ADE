# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_inference.py:7
# Component id: at.source.a1_at_functions.inference
from __future__ import annotations

__version__ = "0.1.0"

def inference(self, prompt: str, **kwargs: Any) -> InferenceResponse:
    """/v1/inference — Llama 3.1 8B via Cloudflare Workers AI. $0.060/call"""
    return self._post_model("/v1/inference", InferenceResponse, {"prompt": prompt, **kwargs})
