# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/scripts/lora_training/serve_lora.py:119
# Component id: at.source.ass_ade.do_get
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
