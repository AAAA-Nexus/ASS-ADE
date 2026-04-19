# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/scripts/lora_train.py:217
# Component id: at.source.ass_ade.upload_adapter
__version__ = "0.1.0"

def upload_adapter(cfg: TrainConfig, adapter_dir: Path) -> tuple[str, str]:
    """Push the adapter artifact to the configured backend.

    Returns (adapter_url, weights_sha256).
    """
    # Compute a content hash over the adapter_model.safetensors for integrity.
    weights_path = adapter_dir / "adapter_model.safetensors"
    if not weights_path.exists():
        # older peft versions use .bin
        weights_path = adapter_dir / "adapter_model.bin"
    if not weights_path.exists():
        raise RuntimeError(f"no adapter weights found under {adapter_dir}")
    sha = hashlib.sha256(weights_path.read_bytes()).hexdigest()

    if cfg.upload_backend == "hf":
        return _upload_hf(cfg, adapter_dir, sha), sha
    if cfg.upload_backend == "r2":
        return _upload_r2(cfg, adapter_dir, sha), sha
    # local: just point at the on-disk path (useful for dev / GH Actions
    # artifact handoff; the Worker obviously can't fetch file:// but a
    # subsequent manual upload can promote the same URL).
    return f"file://{adapter_dir.resolve()}", sha
