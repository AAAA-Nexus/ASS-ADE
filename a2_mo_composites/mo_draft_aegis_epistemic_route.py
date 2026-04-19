# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:561
# Component id: mo.source.a2_mo_composites.aegis_epistemic_route
from __future__ import annotations

__version__ = "0.1.0"

def aegis_epistemic_route(
    self,
    prompt: str | None = None,
    max_tokens: int = 256,
    model: str = "auto",
    *,
    query: str | None = None,
    **kwargs: Any,
) -> EpistemicRouteResult:
    """/v1/aegis/router/epistemic-bound — epistemic-aware routing (AEG-101). $0.040/call"""
    return self._post_model("/v1/aegis/router/epistemic-bound", EpistemicRouteResult, {
        "prompt": prompt or query or "", "max_tokens": max_tokens, "model": model, **kwargs,
    })
