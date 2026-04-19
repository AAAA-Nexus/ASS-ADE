# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/scripts/lora_training/serve_lora.py:130
# Component id: at.source.ass_ade.do_post
__version__ = "0.1.0"

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/generate":
                self._send_json(404, {"error": "not found"})
                return
            length = int(self.headers.get("Content-Length", 0))
            if length == 0:
                self._send_json(400, {"error": "empty body"})
                return
            try:
                body: dict[str, Any] = json.loads(self.rfile.read(length))
            except Exception:
                self._send_json(400, {"error": "invalid JSON"})
                return
            prompt = body.get("prompt", "")
            if not prompt:
                self._send_json(400, {"error": "prompt required"})
                return
            max_new_tokens = int(body.get("max_new_tokens", 256))
            temperature = float(body.get("temperature", 0.7))
            try:
                text = model.generate(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
                self._send_json(200, {
                    "text": text,
                    "model": model.base_model,
                    "tokens": max_new_tokens,
                })
            except Exception as exc:
                _log.exception("generate failed")
                self._send_json(500, {"error": str(exc)})
