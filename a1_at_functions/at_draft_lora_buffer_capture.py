# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_lora_buffer_capture.py:7
# Component id: at.source.a1_at_functions.lora_buffer_capture
from __future__ import annotations

__version__ = "0.1.0"

def lora_buffer_capture(
    self,
    bad: str,
    good: str,
    *,
    language: str = "python",
    lint_delta: float = 0.0,
    **kwargs: Any,
) -> dict[str, Any]:
    """POST /v1/lora/buffer/capture — stream a single (bad, good) pair to the training buffer.

    Preferred over lora_contribute() for single-sample streaming. The server
    batches samples internally and runs periodic training.
    """
    payload: dict[str, Any] = {
        "bad": bad,
        "good": good,
        "language": language,
        "lint_delta": lint_delta,
    }
    payload.update(kwargs)
    return self._post_raw("/v1/lora/buffer/capture", payload)
