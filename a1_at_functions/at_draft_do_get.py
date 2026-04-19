# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_do_get.py:7
# Component id: at.source.a1_at_functions.do_get
from __future__ import annotations

__version__ = "0.1.0"

def do_GET(self) -> None:  # noqa: N802
    if self.path == "/health":
        self._send_json(200, {
            "status": "ok",
            "model": model.base_model,
            "adapter": str(model.adapter_dir),
            "loaded": model._model is not None,
        })
    else:
        self._send_json(404, {"error": "not found"})
