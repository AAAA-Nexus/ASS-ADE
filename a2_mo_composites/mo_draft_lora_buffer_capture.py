# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1414
# Component id: mo.source.ass_ade.lora_buffer_capture
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
