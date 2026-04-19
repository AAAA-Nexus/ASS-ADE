# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:417
# Component id: mo.source.ass_ade.inference
from __future__ import annotations

__version__ = "0.1.0"

def inference(self, prompt: str, **kwargs: Any) -> InferenceResponse:
    """/v1/inference — Llama 3.1 8B via Cloudflare Workers AI. $0.060/call"""
    return self._post_model("/v1/inference", InferenceResponse, {"prompt": prompt, **kwargs})
