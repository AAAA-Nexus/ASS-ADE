# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/scripts/lora_train.py:310
# Component id: at.source.ass_ade.run_pipeline
__version__ = "0.1.0"

def run_pipeline(cfg: TrainConfig) -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s"
    )
    samples = fetch_samples(cfg)
    if len(samples) < cfg.min_samples_to_train:
        _log.warning(
            "only %d samples available (need %d); skipping training",
            len(samples),
            cfg.min_samples_to_train,
        )
        return 0
    adapter_dir = train_adapter(cfg, samples)
    adapter_url, sha = upload_adapter(cfg, adapter_dir)
    metrics = {
        "sample_count": len(samples),
        "epochs": cfg.epochs,
        "lora_rank": cfg.lora_rank,
        "base_model": cfg.base_model,
        "trained_at": int(time.time()),
    }
    promotion = promote_adapter(cfg, adapter_url, sha, metrics)
    _log.info("promotion response: %s", json.dumps(promotion, indent=2))
    # Write a receipt so CI artifacts are easy to grab
    (cfg.output_dir / "last_promotion.json").write_text(
        json.dumps(promotion, indent=2), encoding="utf-8"
    )
    return 1 if promotion.get("promoted") else 0
