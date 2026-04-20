"""Serve the local LoRA adapter via HTTP at localhost:8081.

Loads the base model + PEFT adapter from models/lora_adapter/ (or --adapter-dir)
and exposes a minimal generation endpoint so the ASS-ADE interpreter can call it
for enhanced synthesis.

Endpoint:
    POST http://localhost:8081/generate
    Content-Type: application/json
    Body: {"prompt": "...", "max_new_tokens": 256, "temperature": 0.7}
    Response: {"text": "...", "model": "...", "tokens": 256}

    GET http://localhost:8081/health
    Response: {"status": "ok", "model": "...", "adapter": "..."}

Usage:
    pip install -e ".[lora]"
    python scripts/lora_training/serve_lora.py
    python scripts/lora_training/serve_lora.py --adapter-dir models/lora_adapter --port 8081
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
_log = logging.getLogger("serve_lora")

_DEFAULT_ADAPTER = Path("models/lora_adapter")
_DEFAULT_BASE = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
_DEFAULT_PORT = 8081


class _Model:
    """Lazy-loaded model + tokenizer + adapter."""

    def __init__(self, adapter_dir: Path, base_model: str) -> None:
        self.adapter_dir = adapter_dir
        self.base_model = base_model
        self._model: Any = None
        self._tokenizer: Any = None
        self._lock = threading.Lock()

    def _load(self) -> None:
        import torch
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer

        _log.info("loading tokenizer from %s…", self.adapter_dir)
        self._tokenizer = AutoTokenizer.from_pretrained(
            str(self.adapter_dir), trust_remote_code=True
        )
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

        _log.info("loading base model %s…", self.base_model)
        use_gpu = torch.cuda.is_available()
        base = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            torch_dtype=torch.bfloat16 if use_gpu else torch.float32,
            device_map="auto" if use_gpu else None,
            trust_remote_code=True,
        )
        _log.info("applying LoRA adapter from %s…", self.adapter_dir)
        self._model = PeftModel.from_pretrained(base, str(self.adapter_dir))
        self._model.eval()
        _log.info("model ready")

    def ensure_loaded(self) -> None:
        with self._lock:
            if self._model is None:
                self._load()

    def generate(self, prompt: str, max_new_tokens: int = 256, temperature: float = 0.7) -> str:
        import torch

        self.ensure_loaded()
        assert self._model is not None and self._tokenizer is not None

        inputs = self._tokenizer(prompt, return_tensors="pt")
        use_gpu = next(self._model.parameters()).is_cuda
        if use_gpu:
            inputs = {k: v.cuda() for k, v in inputs.items()}

        with torch.no_grad():
            out = self._model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=max(temperature, 1e-3),
                do_sample=temperature > 0,
                pad_token_id=self._tokenizer.eos_token_id,
            )
        new_tokens = out[0][inputs["input_ids"].shape[-1]:]
        return self._tokenizer.decode(new_tokens, skip_special_tokens=True)


_model_instance: _Model | None = None


def _make_handler(model: _Model) -> type[BaseHTTPRequestHandler]:
    class _Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args: Any) -> None:
            _log.debug(fmt, *args)

        def _send_json(self, code: int, body: dict[str, Any]) -> None:
            data = json.dumps(body, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

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

    return _Handler


def serve(
    adapter_dir: Path = _DEFAULT_ADAPTER,
    base_model: str = _DEFAULT_BASE,
    port: int = _DEFAULT_PORT,
    preload: bool = False,
) -> None:
    """Start the HTTP server. Blocks until KeyboardInterrupt."""
    global _model_instance
    model = _Model(adapter_dir=adapter_dir.resolve(), base_model=base_model)
    _model_instance = model

    if preload:
        _log.info("pre-loading model…")
        model.ensure_loaded()
    else:
        _log.info("lazy loading — model loads on first request")

    handler_cls = _make_handler(model)
    server = HTTPServer(("127.0.0.1", port), handler_cls)
    _log.info("serving at http://127.0.0.1:%d/generate", port)
    _log.info("  POST /generate  {prompt, max_new_tokens, temperature}")
    _log.info("  GET  /health")
    _log.info("  Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _log.info("shutting down")
        server.shutdown()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "--adapter-dir",
        type=Path,
        default=_DEFAULT_ADAPTER,
        help="Path to the PEFT adapter directory (default: models/lora_adapter/).",
    )
    ap.add_argument("--base", default=_DEFAULT_BASE, help="Base model HF id.")
    ap.add_argument("--port", type=int, default=_DEFAULT_PORT, help="HTTP port (default: 8081).")
    ap.add_argument("--preload", action="store_true", help="Load model on startup instead of first request.")
    args = ap.parse_args()

    if not args.adapter_dir.exists():
        print(
            f"[serve] ERROR: adapter not found at {args.adapter_dir}.\n"
            "  Run: ass-ade train --run   (or upload from Colab first)",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        import peft  # noqa: F401
        import transformers  # noqa: F401
    except ImportError:
        print("[serve] ERROR: run pip install -e '.[lora]' first", file=sys.stderr)
        sys.exit(1)

    serve(adapter_dir=args.adapter_dir, base_model=args.base, port=args.port, preload=args.preload)


if __name__ == "__main__":
    main()
