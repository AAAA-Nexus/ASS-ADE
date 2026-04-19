# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/scripts/lora_training/serve_lora.py:163
# Component id: at.source.ass_ade.serve
__version__ = "0.1.0"

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
